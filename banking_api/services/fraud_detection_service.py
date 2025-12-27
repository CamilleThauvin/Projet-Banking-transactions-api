"""Fraud detection service with heuristic-based detection."""

import logging
from typing import List, Tuple

import pandas as pd

from banking_api.models.schemas import (
    FraudByType,
    FraudPrediction,
    FraudPredictionRequest,
    FraudSummary,
)
from banking_api.services.data_loader import get_deleted_ids, get_transactions_df

logger = logging.getLogger(__name__)


def _is_suspicious_transaction(row: pd.Series, df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Check if a transaction is suspicious using heuristics.

    Returns:
        Tuple of (is_suspicious, reasons)
    """
    reasons = []
    is_suspicious = False

    # Heuristic 1: Very high amount (above 95th percentile)
    amount_threshold = df["amount"].quantile(0.95)
    if row["amount"] > amount_threshold:
        reasons.append(f"Amount {row['amount']:.2f} exceeds threshold {amount_threshold:.2f}")
        is_suspicious = True

    # Heuristic 2: Multiple transactions in short time (if we had timestamps)
    client_transactions = df[df["client_id"] == row["client_id"]]
    if len(client_transactions) > 50:  # High transaction frequency
        reasons.append("High transaction frequency for this client")
        is_suspicious = True

    # Heuristic 3: Unusual transaction type for amount
    if row["type"] == "TRANSFER" and row["amount"] > 10000:
        reasons.append("Large transfer transaction")
        is_suspicious = True

    # Heuristic 4: Same client sending to same recipient multiple times
    if row["recipient_id"] is not None:
        same_pair = df[
            (df["client_id"] == row["client_id"])
            & (df["recipient_id"] == row["recipient_id"])
        ]
        if len(same_pair) > 20:
            reasons.append("Repeated transactions to same recipient")
            is_suspicious = True

    return is_suspicious, reasons


def get_fraud_summary() -> FraudSummary:
    """
    Get fraud detection summary.

    Returns:
        FraudSummary with overall fraud statistics
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    if len(df) == 0:
        return FraudSummary(
            total_suspicious=0,
            total_flagged=0,
            fraud_rate=0.0,
            total_amount_at_risk=0.0,
        )

    suspicious_count = 0
    flagged_count = 0
    total_amount_at_risk = 0.0

    for _, row in df.iterrows():
        is_suspicious, reasons = _is_suspicious_transaction(row, df)
        if is_suspicious:
            suspicious_count += 1
            if len(reasons) >= 2:  # Flagged if multiple reasons
                flagged_count += 1
                total_amount_at_risk += float(row["amount"])

    total = len(df)
    fraud_rate = (suspicious_count / total * 100) if total > 0 else 0.0

    return FraudSummary(
        total_suspicious=suspicious_count,
        total_flagged=flagged_count,
        fraud_rate=round(fraud_rate, 2),
        total_amount_at_risk=round(total_amount_at_risk, 2),
    )


def get_fraud_by_type() -> List[FraudByType]:
    """
    Get fraud statistics grouped by transaction type.

    Returns:
        List of FraudByType
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    if len(df) == 0:
        return []

    fraud_by_type = []
    grouped = df.groupby("type")

    for trans_type, group_df in grouped:
        suspicious_count = 0
        flagged_count = 0
        total_amount = 0.0

        for _, row in group_df.iterrows():
            is_suspicious, reasons = _is_suspicious_transaction(row, df)
            if is_suspicious:
                suspicious_count += 1
                if len(reasons) >= 2:
                    flagged_count += 1
            total_amount += float(row["amount"])

        fraud_by_type.append(
            FraudByType(
                type=str(trans_type),
                suspicious_count=suspicious_count,
                flagged_count=flagged_count,
                total_amount=round(total_amount, 2),
            )
        )

    return sorted(fraud_by_type, key=lambda x: x.flagged_count, reverse=True)


def predict_fraud(request: FraudPredictionRequest) -> FraudPrediction:
    """
    Predict fraud for a transaction using heuristics.

    Args:
        request: FraudPredictionRequest with transaction details

    Returns:
        FraudPrediction with risk assessment
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    # Create a mock row for the transaction
    mock_row = pd.Series(
        {
            "id": request.transaction_id or 999999,
            "client_id": request.client_id,
            "recipient_id": request.recipient_id,
            "amount": request.amount,
            "type": request.transaction_type,
        }
    )

    is_suspicious, reasons = _is_suspicious_transaction(mock_row, df)

    # Calculate risk score based on reasons
    risk_score = len(reasons) * 25.0  # 25 points per reason
    if request.amount > df["amount"].quantile(0.95):
        risk_score += 20.0
    if request.amount > df["amount"].quantile(0.99):
        risk_score += 30.0

    risk_score = min(risk_score, 100.0)

    # Confidence based on number of matching patterns
    confidence = min(len(reasons) * 30.0, 100.0) if reasons else 10.0

    return FraudPrediction(
        is_suspicious=is_suspicious,
        risk_score=round(risk_score, 2),
        reasons=reasons if reasons else ["No suspicious patterns detected"],
        confidence=round(confidence, 2),
    )

