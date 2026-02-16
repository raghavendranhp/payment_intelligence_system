from fastapi import APIRouter, HTTPException
from app.schemas.payment_schemas import (
    PaymentSummaryRequest, PaymentSummaryResponse,
    FraudRiskRequest, FraudRiskResponse,
    PaymentAskRequest, PaymentAskResponse,
    PaymentRecommendationResponse
)
from app.services.payment_analyzer import PaymentAnalyzer
from app.services.ai_service import GroqAIService


# Initialize the router and services
router = APIRouter(prefix="/ai", tags=["Payment Intelligence AI"])

analyzer = PaymentAnalyzer()
ai_service = GroqAIService()
# ---------------------------------------------------------
# Payment Behavior Analysis API
# ---------------------------------------------------------
@router.post("/payment-summary", response_model=PaymentSummaryResponse)
async def get_payment_summary(request: PaymentSummaryRequest):
    """
    Generates an AI-driven natural language summary of payment trends.
    """
    #Use Pandas to aggregate metrics
    metrics = analyzer.get_summary_metrics(str(request.start_date), str(request.end_date))
    
    if "error" in metrics:
        raise HTTPException(status_code=404, detail=metrics["error"])
    
    #Pass aggregated metrics to SeShat AI
    ai_summary = ai_service.generate_payment_summary(metrics)
    
    return PaymentSummaryResponse(summary=ai_summary)


# ---------------------------------------------------------
# AI Fraud Risk Explanation 
# ---------------------------------------------------------
@router.post("/fraud-risk", response_model=FraudRiskResponse)
async def explain_fraud_risk(request: FraudRiskRequest):
    """
    Analyzes a specific transaction, calculates heuristic risk, and gets an AI explanation.
    """
    #Use Pandas to find the transaction and calculate base heuristic risk
    risk_data = analyzer.evaluate_fraud_risk(request.transaction_id)
    
    if "error" in risk_data:
        raise HTTPException(status_code=404, detail=risk_data["error"])
    
    #Send the pre-calculated context to SeShat AI for explanation
    ai_result = ai_service.explain_fraud_risk(risk_data)
    
    return FraudRiskResponse(
        risk_score=ai_result["risk_score"],
        explanation=ai_result["explanation"],
        recommendation=ai_result["recommendation"]
    )


# ---------------------------------------------------------
# AI Smart Payment Query (Natural Language)
# ---------------------------------------------------------
@router.post("/payment-ask", response_model=PaymentAskResponse)
async def ask_payment_question(request: PaymentAskRequest):
    """
    Allows business teams to ask questions about the payment data in natural language.
    """
    #Get global dataset context
    global_context = analyzer.get_global_context()
    
    #Send question and context to SeShat AI
    ai_answer = ai_service.answer_payment_query(request.question, global_context)
    
    return PaymentAskResponse(answer=ai_answer)


# ---------------------------------------------------------
# Payment Recommendation Engine
# ---------------------------------------------------------
@router.get("/payment-recommendations", response_model=PaymentRecommendationResponse)
async def get_payment_recommendations():
    """
    Provides proactive AI suggestions for payment optimization and fraud prevention.
    """
    #Get global dataset context
    global_context = analyzer.get_global_context()
    
    #Ask SeShat AI for strategic recommendations
    insights = ai_service.generate_recommendations(global_context)
    
    return PaymentRecommendationResponse(insights=insights)