"""Transactions routes."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from banking_api.models.schemas import (
    PaginatedResponse,
    PaginationParams,
    Transaction,
    TransactionFilters,
    TransactionSearch,
)
from banking_api.services import transactions_service

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=PaginatedResponse)
async def get_transactions(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    type: Optional[str] = Query(None, description="Filter by transaction type"),
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    recipient_id: Optional[int] = Query(None, description="Filter by recipient ID"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum amount"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="Filter by status"),
):
    """
    Get transactions with pagination and filters.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 100)
    - **type**: Filter by transaction type
    - **client_id**: Filter by client ID
    - **recipient_id**: Filter by recipient ID
    - **min_amount**: Minimum transaction amount
    - **max_amount**: Maximum transaction amount
    - **start_date**: Start date filter (YYYY-MM-DD)
    - **end_date**: End date filter (YYYY-MM-DD)
    - **status**: Filter by transaction status
    """
    filters = TransactionFilters(
        type=type,
        client_id=client_id,
        recipient_id=recipient_id,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
        status=status,
    )
    pagination = PaginationParams(page=page, page_size=page_size)

    result = transactions_service.get_transactions(filters=filters, pagination=pagination)
    return PaginatedResponse(**result)


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction(transaction_id: int):
    """
    Get a transaction by ID.

    - **transaction_id**: Transaction ID
    """
    transaction = transactions_service.get_transaction_by_id(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/search", response_model=PaginatedResponse)
async def search_transactions(search: TransactionSearch):
    """
    Search transactions by text query.

    - **query**: Search query string
    - **filters**: Optional transaction filters
    - **pagination**: Optional pagination parameters
    """
    result = transactions_service.search_transactions(
        query=search.query,
        filters=search.filters,
        pagination=search.pagination,
    )
    return PaginatedResponse(**result)


@router.get("/types", response_model=list[str])
async def get_transaction_types():
    """
    Get list of unique transaction types.
    """
    return transactions_service.get_transaction_types()


@router.get("/recent", response_model=list[Transaction])
async def get_recent_transactions(limit: int = Query(10, ge=1, le=100)):
    """
    Get recent transactions.

    - **limit**: Maximum number of transactions (default: 10, max: 100)
    """
    return transactions_service.get_recent_transactions(limit=limit)


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int):
    """
    Delete a transaction (fictitious deletion).

    - **transaction_id**: Transaction ID to delete
    """
    deleted = transactions_service.remove_transaction(transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully", "id": transaction_id}


@router.get("/by-customer/{customer_id}", response_model=list[Transaction])
async def get_transactions_by_customer(customer_id: int):
    """
    Get all transactions for a specific customer (as sender).

    - **customer_id**: Customer ID
    """
    return transactions_service.get_transactions_by_customer(customer_id)


@router.get("/to-customer/{customer_id}", response_model=list[Transaction])
async def get_transactions_to_customer(customer_id: int):
    """
    Get all transactions to a specific customer (as recipient).

    - **customer_id**: Customer ID
    """
    return transactions_service.get_transactions_to_customer(customer_id)

