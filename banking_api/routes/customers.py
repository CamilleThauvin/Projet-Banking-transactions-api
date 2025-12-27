"""Customers routes."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from banking_api.models.schemas import Customer, CustomerSummary
from banking_api.services import customer_service

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("", response_model=list[Customer])
async def get_customers():
    """
    Get all customers with their statistics.

    Returns list of customers with:
    - Total transactions
    - Total amount
    - Average amount
    - Number of cards
    """
    return customer_service.get_customers()


@router.get("/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """
    Get a customer by ID.

    - **customer_id**: Customer ID
    """
    customer = customer_service.get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/top", response_model=list[CustomerSummary])
async def get_top_customers(
    limit: int = Query(10, ge=1, le=100, description="Number of customers"),
    sort_by: str = Query(
        "total_amount",
        description="Sort field: 'total_amount' or 'total_transactions'",
    ),
):
    """
    Get top customers by volume.

    - **limit**: Number of customers to return (default: 10, max: 100)
    - **sort_by**: Sort field - 'total_amount' or 'total_transactions' (default: total_amount)
    """
    if sort_by not in ["total_amount", "total_transactions"]:
        raise HTTPException(
            status_code=422,
            detail="sort_by must be 'total_amount' or 'total_transactions'",
        )
    return customer_service.get_top_customers(limit=limit, sort_by=sort_by)

