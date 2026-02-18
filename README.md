
# AI-Powered Payment Intelligence System (SeShat AI)

This project is an AI-driven payment analysis service built for an e-commerce platform. It uses a decoupled microservices architecture with a **FastAPI** backend and a **Streamlit** frontend to analyze payment risk patterns, generate intelligent insights, and provide natural-language fraud explanations using Groq (Llama 3.1).

## Technology Stack
* **Backend:** Python, FastAPI, SQLite, Pandas
* **Frontend:** Streamlit
* **AI Integration:** Groq API (llama-3.1-8b-instant)



## Project Structure
```text
payment_intelligence_system/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── routers/
│   │   └── payment_routes.py   # API Endpoints
│   ├── services/
│   │   ├── ai_service.py       # Groq AI integration
│   │   └── payment_analyzer.py # Pandas & SQLite math/logic
│   ├── models/
│   │   └── database.py         # SQLite connection logic
│   ├── schemas/
│   │   └── payment_schemas.py  # Pydantic validation models
│   └── prompts/                # AI system and user prompts (.txt)
├── data/
│   └── amazon_payments_seshat_500.csv  # Raw dataset
├── app.py                      # Streamlit frontend application
├── init_db.py                  # Script to convert CSV to SQLite DB
├── requirements.txt            # Project dependencies
└── .env                        # API keys and secrets

```

## Setup Instructions

**1. Install Dependencies**
Ensure you have Python installed, then run:

```bash
pip install -r requirements.txt

```

**2. Set Up Environment Variables**
Create a `.env` file in the root directory and add your Groq API key:

```env
GROQ_API_KEY=your_actual_api_key_here

```

**3. Initialize the Database**
Run the ETL script to convert the raw CSV into an SQLite database (`payments.db`):

```bash
python init_db.py

```

## How to Run the Application

You will need to open **two separate terminal windows** to run the backend and frontend simultaneously.

**Terminal 1: Start the Backend (FastAPI)**

```bash
uvicorn app.main:app --reload

```

*The API will be available at `http://127.0.0.1:8000*`
*Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs*`

**Terminal 2: Start the Frontend (Streamlit)**

```bash
streamlit run app.py

```

*The interactive dashboard will automatically open in your browser at `http://localhost:8501*`

## 🔌 API Endpoints

* `POST /ai/payment-summary`: Generates an AI summary of payment metrics over a specific date range.
* `POST /ai/fraud-risk`: Analyzes a specific transaction ID for heuristic risk factors and provides an AI explanation/recommendation.
* `POST /ai/payment-ask`: Allows natural language Q&A against the global payment dataset.
* `GET /ai/payment-recommendations`: Fetches strategic, dataset-wide optimization suggestions.

