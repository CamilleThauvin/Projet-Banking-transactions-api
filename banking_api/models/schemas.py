"""Pydantic schemas for the Banking Transactions API."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Transaction Models
class Transaction(BaseModel):
    """Transaction model."""

    id: int
    client_id: int = Field(..., description="ID of the client making the transaction")
    recipient_id: Optional[int] = Field(None, description="ID of the recipient client")
    amount: float = Field(..., ge=0, description="Transaction amount")
    type: str = Field(..., description="Transaction type (PURCHASE, PAYMENT, TRANSFER)")
    date: str = Field(..., description="Transaction date (YYYY-MM-DD)")
    timestamp: str = Field(..., description="Transaction timestamp (ISO format)")
    card_id: Optional[int] = Field(None, description="Associated card ID")
    card_brand: Optional[str] = Field(None, description="Card brand (Visa, Mastercard)")
    status: str = Field(..., description="Transaction status (COMPLETED, PENDING)")
    description: Optional[str] = Field(None, description="Transaction description")

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "id": 452400,
                "client_id": 825,
                "recipient_id": 925,
                "amount": 242.95,
                "type": "PURCHASE",
                "date": "2024-01-15",
                "timestamp": "2024-01-15T10:30:00",
                "card_id": 4524,
                "card_brand": "Visa",
                "status": "COMPLETED",
                "description": "Transaction 1 for card 4524",
            }
        }


class TransactionCreate(BaseModel):
    """Transaction creation model."""

    client_id: int
    recipient_id: Optional[int] = None
    amount: float = Field(..., ge=0)
    type: str
    description: Optional[str] = None


class TransactionUpdate(BaseModel):
    """Transaction update model."""

    amount: Optional[float] = Field(None, ge=0)
    type: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None


class TransactionFilters(BaseModel):
    """Transaction filters for search."""

    type: Optional[str] = None
    client_id: Optional[int] = None
    recipient_id: Optional[int] = None
    min_amount: Optional[float] = Field(None, ge=0)
    max_amount: Optional[float] = Field(None, ge=0)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(10, ge=1, le=100, description="Number of items per page")


class PaginatedResponse(BaseModel):
    """Paginated response model."""

    items: List[Transaction]
    total: int
    page: int
    page_size: int
    total_pages: int


class TransactionSearch(BaseModel):
    """Transaction search model."""

    query: str = Field(..., min_length=1, description="Search query")
    filters: Optional[TransactionFilters] = None
    pagination: Optional[PaginationParams] = None


# Customer Models
class Customer(BaseModel):
    """Customer model."""

    id: int
    total_transactions: int = Field(..., description="Total number of transactions")
    total_amount: float = Field(..., ge=0, description="Total transaction amount")
    average_amount: float = Field(..., ge=0, description="Average transaction amount")
    cards_count: int = Field(..., ge=0, description="Number of cards")


class CustomerSummary(BaseModel):
    """Customer summary model."""

    id: int
    total_transactions: int
    total_amount: float
    average_amount: float


# Stats Models
class StatsOverview(BaseModel):
    """Statistics overview model."""

    total_transactions: int
    total_amount: float
    average_amount: float
    min_amount: float
    max_amount: float
    unique_customers: int
    transactions_by_status: dict[str, int]


class AmountDistribution(BaseModel):
    """Amount distribution model."""

    range: str = Field(..., description="Amount range (e.g., '0-100')")
    count: int = Field(..., ge=0, description="Number of transactions in range")
    percentage: float = Field(..., ge=0, le=100, description="Percentage of total")


class StatsByType(BaseModel):
    """Statistics by transaction type."""

    type: str
    count: int
    total_amount: float
    average_amount: float
    percentage: float


class DailyStats(BaseModel):
    """Daily statistics model."""

    date: str = Field(..., description="Date (YYYY-MM-DD)")
    count: int = Field(..., ge=0, description="Number of transactions")
    total_amount: float = Field(..., ge=0, description="Total amount")
    average_amount: float = Field(..., ge=0, description="Average amount")


# Fraud Models
class FraudSummary(BaseModel):
    """Fraud detection summary."""

    total_suspicious: int = Field(..., ge=0, description="Total suspicious transactions")
    total_flagged: int = Field(..., ge=0, description="Total flagged transactions")
    fraud_rate: float = Field(..., ge=0, le=100, description="Fraud rate percentage")
    total_amount_at_risk: float = Field(..., ge=0, description="Total amount at risk")


class FraudByType(BaseModel):
    """Fraud statistics by type."""

    type: str
    suspicious_count: int
    flagged_count: int
    total_amount: float


class FraudPredictionRequest(BaseModel):
    """Fraud prediction request."""

    transaction_id: Optional[int] = None
    amount: float = Field(..., ge=0)
    client_id: int
    transaction_type: str
    recipient_id: Optional[int] = None


class FraudPrediction(BaseModel):
    """Fraud prediction response."""

    is_suspicious: bool
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    reasons: List[str] = Field(..., description="Reasons for suspicion")
    confidence: float = Field(..., ge=0, le=100, description="Confidence level")


# System Models
class SystemHealth(BaseModel):
    """System health status."""

    status: str = Field(..., description="Health status (OK, ERROR)")
    timestamp: str = Field(..., description="Check timestamp")
    data_loaded: bool = Field(..., description="Whether data is loaded")
    transactions_count: int = Field(..., ge=0, description="Number of transactions")


class SystemMetadata(BaseModel):
    """System metadata."""

    version: str
    environment: str
    total_transactions: int
    total_customers: int
    data_source: str
    last_updated: str

