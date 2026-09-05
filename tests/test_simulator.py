"""
Tests for Risk Simulator API Endpoints
"""

import pytest


def test_calculate_risk(client, sample_simulator_request):
    """Test risk calculation"""
    response = client.post("/api/v1/simulator/calculate", json=sample_simulator_request)
    assert response.status_code == 200
    
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert "decision" in data
    assert "confidence" in data
    assert "contributing_factors" in data
    assert "calculation_breakdown" in data
    
    # Validate risk score
    assert 0 <= data["risk_score"] <= 100


def test_calculate_low_risk_scenario(client):
    """Test calculation of low-risk scenario"""
    request = {
        "amount": 1000.0,
        "payment_method": "UPI",
        "velocity_1h": 1,
        "failed_attempts_15m": 0,
        "merchant_risk_level": "LOW",
        "customer_account_age_days": 730
    }
    
    response = client.post("/api/v1/simulator/calculate", json=request)
    assert response.status_code == 200
    
    data = response.json()
    # Should be low risk
    assert data["risk_level"] == "LOW"
    assert data["decision"] == "ALLOW"


def test_calculate_high_risk_scenario(client):
    """Test calculation of high-risk scenario"""
    request = {
        "amount": 100000.0,
        "payment_method": "CARD",
        "velocity_1h": 15,
        "failed_attempts_15m": 5,
        "merchant_risk_level": "HIGH",
        "customer_account_age_days": 1
    }
    
    response = client.post("/api/v1/simulator/calculate", json=request)
    assert response.status_code == 200
    
    data = response.json()
    # Should be high risk
    assert data["risk_level"] == "HIGH"
    assert data["decision"] in ["REQUIRE_REVIEW", "BLOCK_DEMO_PAYMENT"]


def test_get_simulator_presets(client):
    """Test getting simulator presets"""
    response = client.get("/api/v1/simulator/presets")
    assert response.status_code == 200
    
    data = response.json()
    assert "presets" in data
    assert len(data["presets"]) > 0
    
    # Validate preset structure
    for preset in data["presets"]:
        assert "id" in preset
        assert "name" in preset
        assert "parameters" in preset
        assert "expected_outcome" in preset


def test_batch_calculate(client):
    """Test batch risk calculation"""
    scenarios = [
        {
            "amount": 1000.0,
            "payment_method": "UPI",
            "velocity_1h": 1,
            "failed_attempts_15m": 0,
            "merchant_risk_level": "LOW",
            "customer_account_age_days": 365
        },
        {
            "amount": 50000.0,
            "payment_method": "CARD",
            "velocity_1h": 10,
            "failed_attempts_15m": 3,
            "merchant_risk_level": "HIGH",
            "customer_account_age_days": 5
        }
    ]
    
    response = client.post("/api/v1/simulator/batch-calculate", json=scenarios)
    assert response.status_code == 200
    
    data = response.json()
    assert "total_scenarios" in data
    assert "results" in data
    assert "summary" in data
    assert data["total_scenarios"] == 2
    assert len(data["results"]) == 2


def test_simulator_validation(client):
    """Test simulator with invalid parameters"""
    # Invalid amount
    request = {
        "amount": -100,
        "payment_method": "CARD",
        "velocity_1h": 1,
        "failed_attempts_15m": 0,
        "merchant_risk_level": "LOW",
        "customer_account_age_days": 100
    }
    
    response = client.post("/api/v1/simulator/calculate", json=request)
    assert response.status_code == 422


def test_simulator_contributing_factors(client):
    """Test that contributing factors are provided"""
    request = {
        "amount": 75000.0,
        "payment_method": "CARD",
        "velocity_1h": 8,
        "failed_attempts_15m": 2,
        "merchant_risk_level": "MEDIUM",
        "customer_account_age_days": 10
    }
    
    response = client.post("/api/v1/simulator/calculate", json=request)
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["contributing_factors"]) > 0
    assert isinstance(data["calculation_breakdown"], dict)
