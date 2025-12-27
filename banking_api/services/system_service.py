"""System service for health checks and metadata."""

import logging
from datetime import datetime

from banking_api.core.config import settings
from banking_api.models.schemas import SystemHealth, SystemMetadata
from banking_api.services.data_loader import get_transactions_df

logger = logging.getLogger(__name__)


def get_health() -> SystemHealth:
    """
    Get system health status.

    Returns:
        SystemHealth with status and system information
    """
    try:
        df = get_transactions_df()
        data_loaded = True
        transactions_count = len(df)
        status = "OK"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        data_loaded = False
        transactions_count = 0
        status = "ERROR"

    return SystemHealth(
        status=status,
        timestamp=datetime.now().isoformat(),
        data_loaded=data_loaded,
        transactions_count=transactions_count,
    )


def get_metadata() -> SystemMetadata:
    """
    Get system metadata.

    Returns:
        SystemMetadata with version and system information
    """
    try:
        df = get_transactions_df()
        total_transactions = len(df)
        total_customers = df["client_id"].nunique()
    except Exception:
        total_transactions = 0
        total_customers = 0

    return SystemMetadata(
        version=settings.api_version,
        environment=settings.app_env,
        total_transactions=total_transactions,
        total_customers=total_customers,
        data_source=settings.csv_path,
        last_updated=datetime.now().isoformat(),
    )

