"""
Tests for Transaction API Endpoints
"""

import pytest


def test_list_transactions(client):
    """Test listing all transactions"""
    response = client.get("/api/v1/transactions")
    assert response.status_code == 200
    
    data = response.json()
    assert "transactions" in data
    assert "total" in data
    assert data["total"] > 0


def test_list_transactions_with_filters(client):
    """Test transaction listing with filters"""
    # Filter by risk level
    response = client.get("/api/v1/transactions?risk_level=HIGH")
    assert response.status_code == 200
    
    data = response.json()
    for txn in data["transactions"]:
        assert txn["risk_level"] == "HIGH"


def test_list_transactions_by_payment_method(client):
    """Test filtering by payment method"""
    response = client.get("/api/v1/transactions?payment_method=CARD")
    assert response.status_code == 200
    
    data = response.json()
    for txn in data["transactions"]:
        assert txn["method"] == "CARD"


def test_list_transactions_by_amount_range(client):
    """Test filtering by amount range"""
    response = client.get("/api/v1/transactions?min_amount=1000&max_amount=10000")
    assert response.status_code == 200
    
    data = response.json()
    for txn in data["transactions"]:
        assert 1000 <= txn["amount"] <= 10000


def test_get_recent_transactions(client):
    """Test getting recent transactions"""
    response = client.get("/api/v1/transactions/recent?limit=10")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_get_transaction_by_id(client):
    """Test getting specific transaction"""
    # First get a transaction ID
    response = client.get("/api/v1/transactions/recent?limit=1")
    txn_id = response.json()[0]["id"]
    
    # Get that transaction
    response = client.get(f"/api/v1/transactions/{txn_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == txn_id
    assert "risk_score" in data
    assert "signals" in data


def test_get_transaction_not_found(client):
    """Test getting non-existent transaction"""
    response = client.get("/api/v1/transactions/invalid_txn_id")
    assert response.status_code == 404


def test_get_merchant_transactions(client):
    """Test getting transactions for specific merchant"""
    response = client.get("/api/v1/transactions/merchant/merch_001/history")
    assert response.status_code == 200
    
    data = response.json()
    assert "transactions" in data
    for txn in data["transactions"]:
        assert txn["merchant_id"] == "merch_001"


def test_transaction_stats(client):
    """Test transaction statistics endpoint"""
    response = client.get("/api/v1/transactions/stats/summary")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_transactions" in data
    assert "total_volume_inr" in data
    assert "risk_breakdown" in data
    assert "payment_method_breakdown" in data
    assert "decision_breakdown" in data


def test_transaction_risk_score_range(client):
    """Test that transaction risk scores are valid"""
    response = client.get("/api/v1/transactions?page_size=20")
    assert response.status_code == 200
    
    data = response.json()
    for txn in data["transactions"]:
        assert 0 <= txn["risk_score"] <= 100
        assert txn["risk_level"] in ["LOW", "MEDIUM", "HIGH"]
        assert txn["decision"] in ["ALLOW", "MONITOR", "REQUIRE_REVIEW", "BLOCK_DEMO_PAYMENT"]
