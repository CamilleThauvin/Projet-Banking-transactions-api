"""Data loader module for loading CSV data into memory."""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd

from banking_api.core.config import settings

logger = logging.getLogger(__name__)

# Global in-memory storage
_transactions_df: pd.DataFrame | None = None
_deleted_ids: Set[int] = set()


def load_transactions_data() -> pd.DataFrame:
    """
    Load transactions data from CSV file.

    Since the CSV contains card data, we generate fictional transactions
    based on the card information.

    Returns:
        DataFrame containing transactions data

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV file is empty or invalid
    """
    global _transactions_df

    if _transactions_df is not None:
        return _transactions_df

    csv_path = Path(settings.csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info(f"Loading data from {csv_path}")

    try:
        # Load cards data
        cards_df = pd.read_csv(csv_path)

        if cards_df.empty:
            raise ValueError("CSV file is empty")

        # Generate transactions from cards data
        transactions_list = []

        # Generate multiple transactions per card
        for _, card in cards_df.iterrows():
            card_id = int(card["id"])
            client_id = int(card["client_id"])
            credit_limit_str = str(card["credit_limit"]).replace("$", "").replace(",", "")
            try:
                credit_limit = float(credit_limit_str)
            except (ValueError, AttributeError):
                credit_limit = 1000.0

            # Generate 3-5 transactions per card
            num_transactions = 3 + (card_id % 3)  # 3 to 5 transactions

            for i in range(num_transactions):
                # Generate transaction date (within last 2 years)
                days_ago = (card_id * 7 + i * 3) % 730
                transaction_date = datetime.now() - timedelta(days=days_ago)

                # Generate transaction amount (0.1% to 5% of credit limit)
                amount_multiplier = 0.001 + (card_id % 50) / 1000.0
                amount = round(credit_limit * amount_multiplier, 2)

                # Determine transaction type based on card type
                card_type = str(card["card_type"]).lower()
                if "debit" in card_type:
                    transaction_type = "PURCHASE"
                elif "credit" in card_type:
                    transaction_type = "PAYMENT"
                else:
                    transaction_type = "TRANSFER"

                # Generate recipient customer (different from sender)
                recipient_id = (client_id + 100 + i) % 10000
                if recipient_id == client_id:
                    recipient_id = (recipient_id + 1) % 10000

                transaction = {
                    "id": card_id * 100 + i,  # Unique transaction ID
                    "client_id": client_id,
                    "recipient_id": recipient_id,
                    "amount": amount,
                    "type": transaction_type,
                    "date": transaction_date.strftime("%Y-%m-%d"),
                    "timestamp": transaction_date.isoformat(),
                    "card_id": card_id,
                    "card_brand": str(card["card_brand"]),
                    "status": "COMPLETED" if i % 10 != 0 else "PENDING",
                    "description": f"Transaction {i+1} for card {card_id}",
                }
                transactions_list.append(transaction)

        _transactions_df = pd.DataFrame(transactions_list)

        logger.info(f"Loaded {len(_transactions_df)} transactions from {len(cards_df)} cards")
        return _transactions_df

    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty or invalid")
    except Exception as e:
        logger.error(f"Error loading CSV: {e}")
        raise


def get_transactions_df() -> pd.DataFrame:
    """
    Get the cached transactions DataFrame.

    Returns:
        DataFrame containing transactions data
    """
    if _transactions_df is None:
        return load_transactions_data()
    return _transactions_df


def get_deleted_ids() -> Set[int]:
    """
    Get the set of deleted transaction IDs.

    Returns:
        Set of deleted transaction IDs
    """
    return _deleted_ids


def delete_transaction(transaction_id: int) -> bool:
    """
    Mark a transaction as deleted (fictitious deletion).

    Args:
        transaction_id: ID of the transaction to delete

    Returns:
        True if transaction was marked as deleted, False if already deleted
    """
    if transaction_id in _deleted_ids:
        return False
    _deleted_ids.add(transaction_id)
    return True


def reset_deleted_ids() -> None:
    """Reset the deleted IDs set (for testing purposes)."""
    global _deleted_ids
    _deleted_ids = set()

