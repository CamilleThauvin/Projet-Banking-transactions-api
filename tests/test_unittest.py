"""Unittest tests for integration scenarios."""

import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from banking_api.main import app
from banking_api.services.data_loader import reset_deleted_ids

client = TestClient(app)


class TestTransactionWorkflow(unittest.TestCase):
    """Test complete transaction workflow."""

    def setUp(self):
        """Set up test fixtures."""
        reset_deleted_ids()

    def test_complete_transaction_lifecycle(self):
        """Test complete transaction lifecycle: get, search, delete."""
        # Get transactions
        response = client.get("/api/transactions?page_size=1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data["items"]), 0)

        transaction_id = data["items"][0]["id"]

        # Get specific transaction
        response = client.get(f"/api/transactions/{transaction_id}")
        self.assertEqual(response.status_code, 200)
        transaction = response.json()
        self.assertEqual(transaction["id"], transaction_id)

        # Search for transaction
        response = client.post(
            "/api/transactions/search",
            json={"query": str(transaction_id)},
        )
        self.assertEqual(response.status_code, 200)

        # Delete transaction
        response = client.delete(f"/api/transactions/{transaction_id}")
        self.assertEqual(response.status_code, 200)

        # Verify deleted
        response = client.get(f"/api/transactions/{transaction_id}")
        self.assertEqual(response.status_code, 404)


class TestCustomerTransactions(unittest.TestCase):
    """Test customer transaction relationships."""

    def test_customer_transactions_consistency(self):
        """Test that customer transactions are consistent."""
        # Get a customer
        response = client.get("/api/customers")
        self.assertEqual(response.status_code, 200)
        customers = response.json()
        self.assertGreater(len(customers), 0)

        customer_id = customers[0]["id"]

        # Get transactions by customer
        response = client.get(f"/api/transactions/by-customer/{customer_id}")
        self.assertEqual(response.status_code, 200)
        transactions = response.json()

        # Verify all transactions belong to customer
        for transaction in transactions:
            self.assertEqual(transaction["client_id"], customer_id)

        # Get customer stats
        response = client.get(f"/api/customers/{customer_id}")
        self.assertEqual(response.status_code, 200)
        customer = response.json()

        # Verify transaction count matches
        self.assertEqual(customer["total_transactions"], len(transactions))


class TestStatisticsConsistency(unittest.TestCase):
    """Test statistics consistency."""

    def test_stats_overview_consistency(self):
        """Test that stats overview is consistent with transactions."""
        # Get overview
        response = client.get("/api/stats/overview")
        self.assertEqual(response.status_code, 200)
        overview = response.json()

        # Get transactions count
        response = client.get("/api/transactions")
        self.assertEqual(response.status_code, 200)
        transactions_data = response.json()

        # Verify counts match
        self.assertEqual(overview["total_transactions"], transactions_data["total"])

    def test_stats_by_type_consistency(self):
        """Test that stats by type are consistent."""
        # Get stats by type
        response = client.get("/api/stats/by-type")
        self.assertEqual(response.status_code, 200)
        stats_by_type = response.json()

        # Get transaction types
        response = client.get("/api/transactions/types")
        self.assertEqual(response.status_code, 200)
        types = response.json()

        # Verify all types are represented
        stats_types = [stat["type"] for stat in stats_by_type]
        for trans_type in types:
            self.assertIn(trans_type, stats_types)


class TestFraudDetection(unittest.TestCase):
    """Test fraud detection scenarios."""

    def test_fraud_summary_exists(self):
        """Test that fraud summary is generated."""
        response = client.get("/api/fraud/summary")
        self.assertEqual(response.status_code, 200)
        summary = response.json()

        self.assertIn("total_suspicious", summary)
        self.assertIn("fraud_rate", summary)
        self.assertGreaterEqual(summary["fraud_rate"], 0)

    def test_fraud_prediction_high_amount(self):
        """Test fraud prediction for high amount transaction."""
        response = client.post(
            "/api/fraud/predict",
            json={
                "amount": 50000.0,
                "client_id": 825,
                "transaction_type": "TRANSFER",
            },
        )
        self.assertEqual(response.status_code, 200)
        prediction = response.json()

        self.assertIn("is_suspicious", prediction)
        self.assertIn("risk_score", prediction)
        self.assertGreaterEqual(prediction["risk_score"], 0)
        self.assertLessEqual(prediction["risk_score"], 100)


class TestDataLoading(unittest.TestCase):
    """Test data loading scenarios."""

    def test_data_loaded_on_startup(self):
        """Test that data is loaded on startup."""
        response = client.get("/api/system/health")
        self.assertEqual(response.status_code, 200)
        health = response.json()

        self.assertTrue(health["data_loaded"])
        self.assertGreater(health["transactions_count"], 0)

    def test_metadata_contains_data_info(self):
        """Test that metadata contains data information."""
        response = client.get("/api/system/metadata")
        self.assertEqual(response.status_code, 200)
        metadata = response.json()

        self.assertIn("total_transactions", metadata)
        self.assertIn("total_customers", metadata)
        self.assertIn("data_source", metadata)
        self.assertGreater(metadata["total_transactions"], 0)


class TestPagination(unittest.TestCase):
    """Test pagination scenarios."""

    def test_pagination_consistency(self):
        """Test that pagination is consistent."""
        # Get first page
        response = client.get("/api/transactions?page=1&page_size=10")
        self.assertEqual(response.status_code, 200)
        page1 = response.json()

        # Get second page
        response = client.get("/api/transactions?page=2&page_size=10")
        self.assertEqual(response.status_code, 200)
        page2 = response.json()

        # Verify no duplicates
        page1_ids = {item["id"] for item in page1["items"]}
        page2_ids = {item["id"] for item in page2["items"]}
        self.assertEqual(len(page1_ids & page2_ids), 0)

    def test_pagination_total_pages(self):
        """Test that total_pages is calculated correctly."""
        response = client.get("/api/transactions?page=1&page_size=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        expected_pages = (data["total"] + data["page_size"] - 1) // data["page_size"]
        self.assertEqual(data["total_pages"], expected_pages)


if __name__ == "__main__":
    unittest.main()

