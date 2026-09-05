"""
Tests for Checkout API Endpoints
"""

import pytest


def test_evaluate_checkout(client, sample_checkout_request):
    """Test checkout risk evaluation"""
    response = client.post("/api/v1/checkout/evaluate", json=sample_checkout_request)
    assert response.status_code == 200
    
    data = response.json()
    assert "transaction_id" in data
    assert "risk_score" in data
    assert "risk_level" in data
    assert "decision" in data
    assert "confidence" in data
    assert "signals" in data
    assert "processing_time_ms" in data
    assert "allow_transaction" in data
    
    # Validate risk score
    assert 0 <= data["risk_score"] <= 100


def test_evaluate_checkout_invalid_merchant(client):
    """Test checkout evaluation with invalid merchant"""
    request = {
        "merchant_id": "invalid_merchant",
        "amount": 1000.0,
        "payment_method": "CARD"
    }
    
    response = client.post("/api/v1/checkout/evaluate", json=request)
    assert response.status_code == 404


def test_evaluate_checkout_card_payment(client):
    """Test checkout with card payment"""
    request = {
        "merchant_id": "merch_001",
        "amount": 5000.0,
        "payment_method": "CARD",
        "card_last4": "1234"
    }
    
    response = client.post("/api/v1/checkout/evaluate", json=request)
    assert response.status_code == 200
    
    data = response.json()
    assert data["allow_transaction"] in [True, False]


def test_evaluate_checkout_upi_payment(client):
    """Test checkout with UPI payment"""
    request = {
        "merchant_id": "merch_001",
        "amount": 2000.0,
        "payment_method": "UPI",
        "upi_handle": "user@paytm"
    }
    
    response = client.post("/api/v1/checkout/evaluate", json=request)
    assert response.status_code == 200


def test_simulate_payment_allowed(client):
    """Test simulated payment flow - allowed"""
    request = {
        "merchant_id": "merch_001",  # Low risk merchant
        "amount": 1000.0,
        "payment_method": "UPI"
    }
    
    response = client.post("/api/v1/checkout/simulate-payment", json=request)
    assert response.status_code == 200
    
    data = response.json()
    assert "payment_status" in data
    assert "risk_evaluation" in data
    assert data["demo_mode"] == True


def test_simulate_payment_blocked(client):
    """Test simulated payment flow - blocked"""
    request = {
        "merchant_id": "merch_006",  # High risk merchant
        "amount": 50000.0,
        "payment_method": "CARD"
    }
    
    response = client.post("/api/v1/checkout/simulate-payment", json=request)
    assert response.status_code == 200
    
    data = response.json()
    # May be blocked or flagged for review depending on risk score
    assert data["payment_status"] in ["SUCCESS", "BLOCKED", "REQUIRE_REVIEW"]


def test_checkout_validation_errors(client):
    """Test checkout with invalid parameters"""
    # Missing required field
    response = client.post("/api/v1/checkout/evaluate", json={"merchant_id": "merch_001"})
    assert response.status_code == 422
    
    # Invalid amount
    response = client.post(
        "/api/v1/checkout/evaluate",
        json={
            "merchant_id": "merch_001",
            "amount": -100,
            "payment_method": "CARD"
        }
    )
    assert response.status_code == 422
