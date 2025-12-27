"""Fraud detection routes."""

from fastapi import APIRouter

from banking_api.models.schemas import (
    FraudByType,
    FraudPrediction,
    FraudPredictionRequest,
    FraudSummary,
)
from banking_api.services import fraud_detection_service

router = APIRouter(prefix="/api/fraud", tags=["fraud"])


@router.get("/summary", response_model=FraudSummary)
async def get_fraud_summary():
    """
    Get fraud detection summary.

    Returns overall fraud statistics:
    - Total suspicious transactions
    - Total flagged transactions
    - Fraud rate percentage
    - Total amount at risk
    """
    return fraud_detection_service.get_fraud_summary()


@router.get("/by-type", response_model=list[FraudByType])
async def get_fraud_by_type():
    """
    Get fraud statistics grouped by transaction type.

    Returns fraud statistics for each transaction type:
    - Suspicious count
    - Flagged count
    - Total amount
    """
    return fraud_detection_service.get_fraud_by_type()


@router.post("/predict", response_model=FraudPrediction)
async def predict_fraud(request: FraudPredictionRequest):
    """
    Predict fraud for a transaction using heuristics.

    - **transaction_id**: Optional transaction ID
    - **amount**: Transaction amount
    - **client_id**: Client ID
    - **transaction_type**: Transaction type
    - **recipient_id**: Optional recipient ID

    Returns fraud prediction with:
    - Suspicious flag
    - Risk score (0-100)
    - Reasons for suspicion
    - Confidence level
    """
    return fraud_detection_service.predict_fraud(request)

