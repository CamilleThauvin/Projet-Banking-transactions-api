"""Statistics routes."""

from fastapi import APIRouter

from banking_api.models.schemas import (
    AmountDistribution,
    DailyStats,
    StatsByType,
    StatsOverview,
)
from banking_api.services import stats_service

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("/overview", response_model=StatsOverview)
async def get_stats_overview():
    """
    Get overview statistics.

    Returns global statistics including:
    - Total transactions
    - Total amount
    - Average amount
    - Min/Max amounts
    - Unique customers
    - Transactions by status
    """
    return stats_service.get_overview()


@router.get("/amount-distribution", response_model=list[AmountDistribution])
async def get_amount_distribution():
    """
    Get amount distribution by ranges.

    Returns distribution of transactions across amount ranges:
    - 0-100
    - 100-500
    - 500-1000
    - 1000-5000
    - 5000-10000
    - 10000+
    """
    return stats_service.get_amount_distribution()


@router.get("/by-type", response_model=list[StatsByType])
async def get_stats_by_type():
    """
    Get statistics grouped by transaction type.

    Returns statistics for each transaction type:
    - Count
    - Total amount
    - Average amount
    - Percentage of total
    """
    return stats_service.get_stats_by_type()


@router.get("/daily", response_model=list[DailyStats])
async def get_daily_stats():
    """
    Get daily statistics.

    Returns statistics aggregated by day:
    - Date
    - Transaction count
    - Total amount
    - Average amount
    """
    return stats_service.get_daily_stats()

