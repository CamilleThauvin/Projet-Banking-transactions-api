"""Customer service for handling customer operations."""

import logging
from typing import List, Optional

import pandas as pd

from banking_api.core.config import settings
from banking_api.models.schemas import Customer, CustomerSummary
from banking_api.services.data_loader import get_deleted_ids, get_transactions_df

logger = logging.getLogger(__name__)


def get_customers() -> List[Customer]:
    """
    Get all customers with their statistics.

    Returns:
        List of Customer objects
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    # Group by client_id
    customer_stats = df.groupby("client_id").agg(
        {
            "id": "count",  # total transactions
            "amount": ["sum", "mean"],  # total and average amount
        }
    ).reset_index()

    customer_stats.columns = ["id", "total_transactions", "total_amount", "average_amount"]

    # Get card counts (from original data structure)
    cards_df = pd.read_csv(settings.csv_path)
    card_counts = cards_df.groupby("client_id")["id"].count().reset_index()
    card_counts.columns = ["client_id", "cards_count"]

    # Merge
    customer_stats = customer_stats.merge(
        card_counts, left_on="id", right_on="client_id", how="left"
    )
    customer_stats["cards_count"] = customer_stats["cards_count"].fillna(0).astype(int)

    customers = []
    for _, row in customer_stats.iterrows():
        customers.append(
            Customer(
                id=int(row["id"]),
                total_transactions=int(row["total_transactions"]),
                total_amount=float(row["total_amount"]),
                average_amount=float(row["average_amount"]),
                cards_count=int(row["cards_count"]),
            )
        )

    return sorted(customers, key=lambda x: x.id)


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    """
    Get a customer by ID.

    Args:
        customer_id: Customer ID

    Returns:
        Customer if found, None otherwise
    """
    customers = get_customers()
    for customer in customers:
        if customer.id == customer_id:
            return customer
    return None


def get_top_customers(limit: int = 10, sort_by: str = "total_amount") -> List[CustomerSummary]:
    """
    Get top customers by volume.

    Args:
        limit: Number of customers to return
        sort_by: Sort field ('total_amount' or 'total_transactions')

    Returns:
        List of CustomerSummary objects
    """
    customers = get_customers()

    if sort_by == "total_transactions":
        customers.sort(key=lambda x: x.total_transactions, reverse=True)
    else:  # default to total_amount
        customers.sort(key=lambda x: x.total_amount, reverse=True)

    top_customers = customers[:limit]

    return [
        CustomerSummary(
            id=c.id,
            total_transactions=c.total_transactions,
            total_amount=c.total_amount,
            average_amount=c.average_amount,
        )
        for c in top_customers
    ]

