"""Statistics service for computing transaction statistics."""

import logging
from typing import Dict, List

import pandas as pd

from banking_api.models.schemas import (
    AmountDistribution,
    DailyStats,
    StatsByType,
    StatsOverview,
)
from banking_api.services.data_loader import get_deleted_ids, get_transactions_df

logger = logging.getLogger(__name__)


def get_overview() -> StatsOverview:
    """
    Get overview statistics.

    Returns:
        StatsOverview with global statistics
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    total_transactions = len(df)
    total_amount = float(df["amount"].sum())
    average_amount = float(df["amount"].mean()) if total_transactions > 0 else 0.0
    min_amount = float(df["amount"].min()) if total_transactions > 0 else 0.0
    max_amount = float(df["amount"].max()) if total_transactions > 0 else 0.0
    unique_customers = df["client_id"].nunique()

    transactions_by_status = df["status"].value_counts().to_dict()
    transactions_by_status = {str(k): int(v) for k, v in transactions_by_status.items()}

    return StatsOverview(
        total_transactions=total_transactions,
        total_amount=total_amount,
        average_amount=average_amount,
        min_amount=min_amount,
        max_amount=max_amount,
        unique_customers=unique_customers,
        transactions_by_status=transactions_by_status,
    )


def get_amount_distribution() -> List[AmountDistribution]:
    """
    Get amount distribution by ranges.

    Returns:
        List of AmountDistribution by range
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    total = len(df)
    if total == 0:
        return []

    # Define ranges
    ranges = [
        (0, 100),
        (100, 500),
        (500, 1000),
        (1000, 5000),
        (5000, 10000),
        (10000, float("inf")),
    ]

    distributions = []
    for min_val, max_val in ranges:
        if max_val == float("inf"):
            mask = df["amount"] >= min_val
            range_str = f"{min_val}+"
        else:
            mask = (df["amount"] >= min_val) & (df["amount"] < max_val)
            range_str = f"{min_val}-{max_val}"

        count = int(mask.sum())
        percentage = (count / total * 100) if total > 0 else 0.0

        distributions.append(
            AmountDistribution(
                range=range_str,
                count=count,
                percentage=round(percentage, 2),
            )
        )

    return distributions


def get_stats_by_type() -> List[StatsByType]:
    """
    Get statistics grouped by transaction type.

    Returns:
        List of StatsByType
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    total = len(df)
    if total == 0:
        return []

    stats_list = []
    grouped = df.groupby("type")

    for trans_type, group_df in grouped:
        count = len(group_df)
        total_amount = float(group_df["amount"].sum())
        average_amount = float(group_df["amount"].mean())
        percentage = (count / total * 100) if total > 0 else 0.0

        stats_list.append(
            StatsByType(
                type=str(trans_type),
                count=count,
                total_amount=total_amount,
                average_amount=average_amount,
                percentage=round(percentage, 2),
            )
        )

    return sorted(stats_list, key=lambda x: x.count, reverse=True)


def get_daily_stats() -> List[DailyStats]:
    """
    Get daily statistics.

    Returns:
        List of DailyStats ordered by date
    """
    df = get_transactions_df()
    deleted_ids = get_deleted_ids()
    df = df[~df["id"].isin(deleted_ids)]

    if len(df) == 0:
        return []

    # Group by date
    daily = df.groupby("date").agg(
        {
            "amount": ["count", "sum", "mean"],
        }
    ).reset_index()

    daily.columns = ["date", "count", "total_amount", "average_amount"]

    daily_stats = []
    for _, row in daily.iterrows():
        daily_stats.append(
            DailyStats(
                date=str(row["date"]),
                count=int(row["count"]),
                total_amount=float(row["total_amount"]),
                average_amount=float(row["average_amount"]),
            )
        )

    # Sort by date descending
    daily_stats.sort(key=lambda x: x.date, reverse=True)

    return daily_stats

