"""System routes."""

from fastapi import APIRouter

from banking_api.models.schemas import SystemHealth, SystemMetadata
from banking_api.services import system_service

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/health", response_model=SystemHealth)
async def get_health():
    """
    Get system health status.

    Returns:
    - Status (OK/ERROR)
    - Timestamp
    - Data loaded flag
    - Transactions count
    """
    return system_service.get_health()


@router.get("/metadata", response_model=SystemMetadata)
async def get_metadata():
    """
    Get system metadata.

    Returns:
    - API version
    - Environment
    - Total transactions
    - Total customers
    - Data source path
    - Last updated timestamp
    """
    return system_service.get_metadata()

