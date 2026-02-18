import streamlit as st
import requests
from datetime import date

# ---------------------------------------------------------
# Configuration & Setup
# ---------------------------------------------------------
st.set_page_config(page_title="AI Payment Intelligence", page_icon="💸", layout="wide")

# Point this to your local FastAPI server
API_URL = "http://127.0.0.1:8000/ai"

st.title(" AI Payment Intelligence Dashboard")
st.markdown("Interact with the SeShat/Groq AI models via the decoupled FastAPI backend.")

# Create a clean tabbed layout for the 4 endpoints
tab1, tab2, tab3, tab4 = st.tabs([
    " 1. Payment Summary", 
    " 2. Fraud Risk", 
    " 3. Smart Query", 
    " 4. Recommendations"
])

# ---------------------------------------------------------
# Tab 1: Payment Behavior Analysis (POST /payment-summary)
# ---------------------------------------------------------
with tab1:
    st.header("Payment Behavior Analysis")
    st.write("Generate an AI summary of payment metrics over a specific timeframe.")
    
    col1, col2 = st.columns(2)
    with col1:
        # Setting defaults to match your dataset
        start_date = st.date_input("Start Date", value=date(2026, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=date(2026, 3, 31))
        
    if st.button("Generate Summary", type="primary"):
        with st.spinner("Crunching Pandas metrics and generating AI summary..."):
            payload = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            }
            try:
                response = requests.post(f"{API_URL}/payment-summary", json=payload)
                if response.status_code == 200:
                    st.success("Analysis Complete!")
                    st.info(response.json().get("summary", "No summary returned."))
                else:
                    st.error(f"Backend Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Is `uvicorn app.main:app` running?")

# ---------------------------------------------------------
# Tab 2: AI Fraud Risk Explanation (POST /fraud-risk)
# ---------------------------------------------------------
with tab2:
    st.header("AI Fraud Risk Explanation")
    st.write("Analyze a specific transaction for heuristic risk factors and AI explanations.")
    
    
    tx_id = st.text_input("Transaction ID", value="TX10031")
    
    if st.button("Analyze Risk", type="primary"):
        with st.spinner("Evaluating risk patterns with AI..."):
            try:
                response = requests.post(f"{API_URL}/fraud-risk", json={"transaction_id": tx_id})
                if response.status_code == 200:
                    data = response.json()
                    
                    st.subheader("Results")
                    # Dynamically color the risk score
                    risk = data.get("risk_score", "Unknown")
                    if risk == "High":
                        st.error(f"**Risk Score:** {risk}")
                    elif risk == "Medium":
                        st.warning(f"**Risk Score:** {risk}")
                    else:
                        st.success(f"**Risk Score:** {risk}")
                        
                    st.write(f"**AI Explanation:** {data.get('explanation')}")
                    
                    # Call to action metric
                    action = data.get('recommendation', '').upper()
                    st.metric(label="Suggested Action", value=action)
                else:
                    st.error(f"Backend Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Is the backend server running?")

# ---------------------------------------------------------
# Tab 3: AI Smart Payment Query (POST /payment-ask)
# ---------------------------------------------------------
with tab3:
    st.header("Smart Payment Query")
    st.write("Ask natural language questions about the global dataset context.")
    
    question = st.text_input("Your Question", value="Why are payment failures increasing this month?")
    
    if st.button("Ask AI Analyst", type="primary"):
        with st.spinner("Analyzing global metrics to answer your query..."):
            try:
                response = requests.post(f"{API_URL}/payment-ask", json={"question": question})
                if response.status_code == 200:
                    st.success("Answered!")
                    st.write(response.json().get("answer", "No answer returned."))
                else:
                    st.error(f"Backend Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Is the backend server running?")

# ---------------------------------------------------------
# Tab 4: Payment Recommendations (GET /payment-recommendations)
# ---------------------------------------------------------
with tab4:
    st.header("Proactive AI Recommendations")
    st.write("Fetch strategic, dataset-wide optimization suggestions from the AI.")
    
    if st.button("Fetch Recommendations", type="primary"):
        with st.spinner("Generating insights..."):
            try:
                # Notice this is a GET request, so no JSON payload is sent
                response = requests.get(f"{API_URL}/payment-recommendations")
                if response.status_code == 200:
                    st.success("Insights Generated!")
                    st.write(response.json().get("insights", "No insights returned."))
                else:
                    st.error(f"Backend Error: {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to FastAPI. Is the backend server running?")
