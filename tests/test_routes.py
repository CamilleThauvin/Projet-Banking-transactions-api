"""Pytest tests for API routes."""

import pytest
from fastapi.testclient import TestClient

from banking_api.main import app

client = TestClient(app)


# Transactions endpoints tests
def test_get_transactions():
    """Test GET /api/transactions."""
    response = client.get("/api/transactions")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data


def test_get_transactions_with_pagination():
    """Test GET /api/transactions with pagination."""
    response = client.get("/api/transactions?page=1&page_size=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 5
    assert data["page"] == 1
    assert data["page_size"] == 5


def test_get_transactions_with_filters():
    """Test GET /api/transactions with filters."""
    response = client.get("/api/transactions?type=PURCHASE&min_amount=100")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        assert data["items"][0]["type"] == "PURCHASE"
        assert data["items"][0]["amount"] >= 100


def test_get_transaction_by_id():
    """Test GET /api/transactions/{id}."""
    # First get a transaction ID
    response = client.get("/api/transactions?page_size=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        transaction_id = data["items"][0]["id"]
        response = client.get(f"/api/transactions/{transaction_id}")
        assert response.status_code == 200
        assert response.json()["id"] == transaction_id


def test_get_transaction_by_id_not_found():
    """Test GET /api/transactions/{id} with non-existent ID."""
    response = client.get("/api/transactions/999999999")
    assert response.status_code == 404


def test_search_transactions():
    """Test POST /api/transactions/search."""
    response = client.post(
        "/api/transactions/search",
        json={"query": "PURCHASE", "pagination": {"page": 1, "page_size": 10}},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


def test_get_transaction_types():
    """Test GET /api/transactions/types."""
    response = client.get("/api/transactions/types")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recent_transactions():
    """Test GET /api/transactions/recent."""
    response = client.get("/api/transactions/recent?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5


def test_delete_transaction():
    """Test DELETE /api/transactions/{id}."""
    # First get a transaction ID
    response = client.get("/api/transactions?page_size=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        transaction_id = data["items"][0]["id"]
        response = client.delete(f"/api/transactions/{transaction_id}")
        assert response.status_code == 200
        # Verify it's deleted
        response = client.get(f"/api/transactions/{transaction_id}")
        assert response.status_code == 404


def test_delete_transaction_not_found():
    """Test DELETE /api/transactions/{id} with non-existent ID."""
    response = client.delete("/api/transactions/999999999")
    assert response.status_code == 404


def test_get_transactions_by_customer():
    """Test GET /api/transactions/by-customer/{customer_id}."""
    # First get a customer ID from transactions
    response = client.get("/api/transactions?page_size=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"]:
        customer_id = data["items"][0]["client_id"]
        response = client.get(f"/api/transactions/by-customer/{customer_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


def test_get_transactions_to_customer():
    """Test GET /api/transactions/to-customer/{customer_id}."""
    # First get a recipient ID from transactions
    response = client.get("/api/transactions?page_size=1")
    assert response.status_code == 200
    data = response.json()
    if data["items"] and data["items"][0].get("recipient_id"):
        recipient_id = data["items"][0]["recipient_id"]
        response = client.get(f"/api/transactions/to-customer/{recipient_id}")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# Stats endpoints tests
def test_get_stats_overview():
    """Test GET /api/stats/overview."""
    response = client.get("/api/stats/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_transactions" in data
    assert "total_amount" in data
    assert "average_amount" in data


def test_get_amount_distribution():
    """Test GET /api/stats/amount-distribution."""
    response = client.get("/api/stats/amount-distribution")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats_by_type():
    """Test GET /api/stats/by-type."""
    response = client.get("/api/stats/by-type")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_daily_stats():
    """Test GET /api/stats/daily."""
    response = client.get("/api/stats/daily")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Fraud endpoints tests
def test_get_fraud_summary():
    """Test GET /api/fraud/summary."""
    response = client.get("/api/fraud/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_suspicious" in data
    assert "total_flagged" in data
    assert "fraud_rate" in data


def test_get_fraud_by_type():
    """Test GET /api/fraud/by-type."""
    response = client.get("/api/fraud/by-type")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_predict_fraud():
    """Test POST /api/fraud/predict."""
    response = client.post(
        "/api/fraud/predict",
        json={
            "amount": 5000.0,
            "client_id": 825,
            "transaction_type": "PURCHASE",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "is_suspicious" in data
    assert "risk_score" in data
    assert "reasons" in data


# Customers endpoints tests
def test_get_customers():
    """Test GET /api/customers."""
    response = client.get("/api/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer_by_id():
    """Test GET /api/customers/{customer_id}."""
    # First get a customer ID
    response = client.get("/api/customers")
    assert response.status_code == 200
    customers = response.json()
    if customers:
        customer_id = customers[0]["id"]
        response = client.get(f"/api/customers/{customer_id}")
        assert response.status_code == 200
        assert response.json()["id"] == customer_id


def test_get_customer_by_id_not_found():
    """Test GET /api/customers/{customer_id} with non-existent ID."""
    response = client.get("/api/customers/999999")
    assert response.status_code == 404


def test_get_top_customers():
    """Test GET /api/customers/top."""
    response = client.get("/api/customers/top?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 5


# System endpoints tests
def test_get_health():
    """Test GET /api/system/health."""
    response = client.get("/api/system/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "timestamp" in data
    assert "data_loaded" in data


def test_get_metadata():
    """Test GET /api/system/metadata."""
    response = client.get("/api/system/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "environment" in data
    assert "total_transactions" in data


# Root endpoint test
def test_root():
    """Test GET /."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

