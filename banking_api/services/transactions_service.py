"""Transactions service for handling transaction operations."""

import logging
from typing import Dict, List, Optional

import pandas as pd

from banking_api.models.schemas import (
    PaginationParams,
    Transaction,
    TransactionFilters,
)
from banking_api.services.data_loader import (
    delete_transaction,
    get_deleted_ids,
    get_transactions_df,
)

logger = logging.getLogger(__name__)


def _dataframe_to_transaction(row: pd.Series) -> Transaction:
    """Convert a DataFrame row to a Transaction model."""
    return Transaction(
        id=int(row["id"]),
        client_id=int(row["client_id"]),
        recipient_id=int(row["recipient_id"]) if pd.notna(row["recipient_id"]) else None,
        amount=float(row["amount"]),
        type=str(row["type"]),
        date=str(row["date"]),
        timestamp=str(row["timestamp"]),
        card_id=int(row["card_id"]) if pd.notna(row["card_id"]) else None,
        card_brand=str(row["card_brand"]) if pd.notna(row["card_brand"]) else None,
        status=str(row["status"]),
        description=str(row["description"]) if pd.notna(row["description"]) else None,
    )


def get_transactions(
    filters: Optional[TransactionFilters] = None,
    pagination: Optional[PaginationParams] = None,
) -> Dict:
    """
    Get transactions with optional filters and pagination.

    Args:
        filters: Optional transaction filters
        pagination: Optional pagination parameters

    Returns:
        Dictionary with paginated transactions and metadata
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()

    # Filter out deleted transactions
    df = df[~df["id"].isin(deleted_ids)]

    # Apply filters
    if filters:
        if filters.type:
            df = df[df["type"] == filters.type]
        if filters.client_id:
            df = df[df["client_id"] == filters.client_id]
        if filters.recipient_id:
            df = df[df["recipient_id"] == filters.recipient_id]
        if filters.min_amount is not None:
            df = df[df["amount"] >= filters.min_amount]
        if filters.max_amount is not None:
            df = df[df["amount"] <= filters.max_amount]
        if filters.start_date:
            df = df[df["date"] >= filters.start_date]
        if filters.end_date:
            df = df[df["date"] <= filters.end_date]
        if filters.status:
            df = df[df["status"] == filters.status]

    # Sort by date descending
    df = df.sort_values("date", ascending=False)

    total = len(df)

    # Apply pagination
    if pagination:
        page = pagination.page
        page_size = pagination.page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        df = df.iloc[start_idx:end_idx]
        total_pages = (total + page_size - 1) // page_size
    else:
        page = 1
        page_size = total
        total_pages = 1

    transactions = [_dataframe_to_transaction(row) for _, row in df.iterrows()]

    return {
        "items": transactions,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_transaction_by_id(transaction_id: int) -> Optional[Transaction]:
    """
    Get a transaction by ID.

    Args:
        transaction_id: Transaction ID

    Returns:
        Transaction if found, None otherwise
    """
    deleted_ids = get_deleted_ids()
    if transaction_id in deleted_ids:
        return None

    df = get_transactions_df()
    result = df[df["id"] == transaction_id]

    if result.empty:
        return None

    return _dataframe_to_transaction(result.iloc[0])


def search_transactions(
    query: str,
    filters: Optional[TransactionFilters] = None,
    pagination: Optional[PaginationParams] = None,
) -> Dict:
    """
    Search transactions by text query.

    Args:
        query: Search query string
        filters: Optional transaction filters
        pagination: Optional pagination parameters

    Returns:
        Dictionary with paginated search results
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()

    # Filter out deleted transactions
    df = df[~df["id"].isin(deleted_ids)]

    # Apply filters first
    if filters:
        if filters.type:
            df = df[df["type"] == filters.type]
        if filters.client_id:
            df = df[df["client_id"] == filters.client_id]
        if filters.recipient_id:
            df = df[df["recipient_id"] == filters.recipient_id]
        if filters.min_amount is not None:
            df = df[df["amount"] >= filters.min_amount]
        if filters.max_amount is not None:
            df = df[df["amount"] <= filters.max_amount]
        if filters.start_date:
            df = df[df["date"] >= filters.start_date]
        if filters.end_date:
            df = df[df["date"] <= filters.end_date]
        if filters.status:
            df = df[df["status"] == filters.status]

    # Text search in description and type
    query_lower = query.lower()
    mask = (
        df["description"].astype(str).str.lower().str.contains(query_lower, na=False)
        | df["type"].astype(str).str.lower().str.contains(query_lower, na=False)
    )
    df = df[mask]

    # Sort by date descending
    df = df.sort_values("date", ascending=False)

    total = len(df)

    # Apply pagination
    if pagination:
        page = pagination.page
        page_size = pagination.page_size
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        df = df.iloc[start_idx:end_idx]
        total_pages = (total + page_size - 1) // page_size
    else:
        page = 1
        page_size = total
        total_pages = 1

    transactions = [_dataframe_to_transaction(row) for _, row in df.iterrows()]

    return {
        "items": transactions,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


def get_transaction_types() -> List[str]:
    """
    Get list of unique transaction types.

    Returns:
        List of unique transaction types
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]
    return sorted(df["type"].unique().tolist())


def get_recent_transactions(limit: int = 10) -> List[Transaction]:
    """
    Get recent transactions.

    Args:
        limit: Maximum number of transactions to return

    Returns:
        List of recent transactions
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]
    df = df.sort_values("date", ascending=False).head(limit)
    return [_dataframe_to_transaction(row) for _, row in df.iterrows()]


def remove_transaction(transaction_id: int) -> bool:
    """
    Delete a transaction (fictitious deletion).

    Args:
        transaction_id: Transaction ID to delete

    Returns:
        True if deleted, False if not found
    """
    transaction = get_transaction_by_id(transaction_id)
    if transaction is None:
        return False
    return delete_transaction(transaction_id)


def get_transactions_by_customer(customer_id: int) -> List[Transaction]:
    """
    Get all transactions for a specific customer (as sender).

    Args:
        customer_id: Customer ID

    Returns:
        List of transactions
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]
    df = df[df["client_id"] == customer_id]
    df = df.sort_values("date", ascending=False)
    return [_dataframe_to_transaction(row) for _, row in df.iterrows()]


def get_transactions_to_customer(customer_id: int) -> List[Transaction]:
    """
    Get all transactions to a specific customer (as recipient).

    Args:
        customer_id: Customer ID

    Returns:
        List of transactions
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]
    df = df[df["recipient_id"] == customer_id]
    df = df.sort_values("date", ascending=False)
    return [_dataframe_to_transaction(row) for _, row in df.iterrows()]

