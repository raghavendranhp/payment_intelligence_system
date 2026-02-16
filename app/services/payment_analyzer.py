import pandas as pd
from datetime import datetime
from app.models.database import get_db_connection

class PaymentAnalyzer:
    def __init__(self):
        """
        Initializes the analyzer by verifying the database connection.
        If the database is missing, the application will fail fast.
        """
        with get_db_connection() as conn:
            pass

    def get_summary_metrics(self, start_date: str, end_date: str) -> dict:
        """
        Aggregates data for the /ai/payment-summary endpoint.
        Uses SQL to filter the exact date range before passing to Pandas.
        """
        
        query = '''
            SELECT payment_status, country, payment_method, amount 
            FROM transactions 
            WHERE transaction_time >= ? AND transaction_time <= ?
        '''
        
        with get_db_connection() as conn:
            
            period_df = pd.read_sql(query, conn, params=(start_date, end_date)) 

        if period_df.empty:
            return {"error": "No transactions found in this date range."}

        total_tx = len(period_df)
        statuses = period_df['payment_status'].value_counts()
        
        success_rate = (statuses.get('Success', 0) / total_tx) * 100
        failure_rate = (statuses.get('Failed', 0) / total_tx) * 100

        #High-risk regions (Countries with highest failure counts)
        failed_df = period_df[period_df['payment_status'] == 'Failed']
        risky_regions = failed_df['country'].value_counts().head(3).to_dict()

        #Payment method performance
        method_perf = period_df.groupby('payment_method')['payment_status'].apply(
            lambda x: (x == 'Success').mean() * 100
        ).to_dict()

        return {
            "total_transactions": total_tx,
            "success_rate_percent": round(success_rate, 2),
            "failure_rate_percent": round(failure_rate, 2),
            "top_failing_regions": risky_regions,
            "payment_method_success_rates": method_perf,
            "total_revenue": period_df[period_df['payment_status'] == 'Success']['amount'].sum()
        }

    def evaluate_fraud_risk(self, transaction_id: str) -> dict:
        """
        Applies heuristic logic for the /ai/fraud-risk endpoint using precise SQL queries
        to fetch only the required context, saving massive amounts of memory.
        """
        with get_db_connection() as conn:
            #Fetch only the specific transaction row requested
            tx_query = "SELECT * FROM transactions WHERE transaction_id = ?"
            tx_df = pd.read_sql(tx_query, conn, params=(transaction_id,))
            
            if tx_df.empty:
                return {"error": "Transaction not found."}

            tx = tx_df.iloc[0]
            customer_id = str(tx['customer_id'])
            
            #Fetch only the historical statuses for this specific customer
            hist_query = "SELECT payment_status FROM transactions WHERE customer_id = ?"
            customer_history = pd.read_sql(hist_query, conn, params=(customer_id,))
            
            # Fetch successful amounts to calculate the global 90th percentile
            amt_query = "SELECT amount FROM transactions WHERE payment_status = 'Success'"
            successful_amounts = pd.read_sql(amt_query, conn)
            
        #Apply the ML/Pandas Math
        
        high_amount_threshold = successful_amounts['amount'].quantile(0.90)
        is_high_amount = tx['amount'] > high_amount_threshold

        past_failures = len(customer_history[customer_history['payment_status'] == 'Failed'])
        high_retries = tx['retry_attempts'] >= 3

        #Calculate Heuristic Risk Score
        risk_points = 0
        if is_high_amount: risk_points += 1
        if past_failures > 2: risk_points += 1
        if high_retries: risk_points += 2

        if risk_points >= 3:
            risk_score = "High"
        elif risk_points >= 1:
            risk_score = "Medium"
        else:
            risk_score = "Low"

        return {
            "transaction_data": tx.to_dict(),
            "indicators": {
                "amount_above_90th_percentile": bool(is_high_amount),
                "past_failures_for_customer": int(past_failures),
                "excessive_retries": bool(high_retries)
            },
            "heuristic_risk_score": risk_score
        }

    def get_global_context(self) -> dict:
        """
        Provides aggregated, system-wide metrics.
        We run a light SQL query to fetch just the specific columns needed for the math.
        """
        query = "SELECT amount, payment_status, device_type, retry_attempts FROM transactions"
        
        with get_db_connection() as conn:
            df = pd.read_sql(query, conn)
            
        return {
            "total_processed_volume": df[df['payment_status'] == 'Success']['amount'].sum(),
            "average_transaction_value": df['amount'].mean(),
            "overall_failure_rate": (len(df[df['payment_status'] == 'Failed']) / len(df)) * 100,
            "most_used_device": df['device_type'].mode()[0] if not df.empty else "Unknown",
            "average_retries": df['retry_attempts'].mean()
        }