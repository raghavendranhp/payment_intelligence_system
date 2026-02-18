import pandas as pd
import sqlite3
import os

def create_database_from_csv():
    csv_path = "data/amazon_payments_seshat_500.csv"
    db_path = "data/payments.db"

    #Check if the CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}. Please ensure the file is in the data folder.")
        return

    #Read the CSV using Pandas
    print("Reading CSV data...")
    df = pd.read_csv(csv_path)
    
    #Connect to SQLite (this automatically creates the .db file if it doesn't exist)
    print("Connecting to SQLite database...")
    conn = sqlite3.connect(db_path)
    
    #Write the Pandas DataFrame into a SQL table named 'transactions'
    print("Writing data to SQLite table 'transactions'...")
   
    df.to_sql("transactions", conn, if_exists="replace", index=False)
    
    Verify it worked
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    row_count = cursor.fetchone()[0]
    
    conn.close()
    print(f"Success! Database created at '{db_path}' with {row_count} rows.")

if __name__ == "__main__":
    # Create the data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    create_database_from_csv()
