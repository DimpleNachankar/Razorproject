"""
Tests for Merchant API Endpoints
"""

import pytest


def test_list_merchants(client):
    """Test listing all merchants"""
    response = client.get("/api/v1/merchants")
    assert response.status_code == 200
    
    data = response.json()
    assert "merchants" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert data["total"] > 0


def test_list_merchants_with_filters(client):
    """Test merchant listing with filters"""
    # Filter by risk level
    response = client.get("/api/v1/merchants?risk_level=LOW")
    assert response.status_code == 200
    
    data = response.json()
    for merchant in data["merchants"]:
        assert merchant["risk_level"] == "LOW"


def test_list_merchants_pagination(client):
    """Test merchant pagination"""
    response = client.get("/api/v1/merchants?page=1&page_size=5")
    assert response.status_code == 200
    
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["merchants"]) <= 5


def test_get_merchant_by_id(client):
    """Test getting merchant by ID"""
    response = client.get("/api/v1/merchants/merch_001")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == "merch_001"
    assert "name" in data
    assert "domain" in data
    assert "risk_score" in data
    assert "signals" in data


def test_get_merchant_by_id_not_found(client):
    """Test getting non-existent merchant"""
    response = client.get("/api/v1/merchants/invalid_id")
    assert response.status_code == 404
    
    data = response.json()
    assert "error" in data


def test_get_merchant_by_domain(client, sample_merchant_domain):
    """Test getting merchant by domain"""
    response = client.get(f"/api/v1/merchants/domain/{sample_merchant_domain}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["domain"] == sample_merchant_domain


def test_analyze_merchant_existing(client, sample_merchant_domain):
    """Test analyzing existing merchant"""
    response = client.post(
        "/api/v1/merchants/analyze",
        json={"domain": sample_merchant_domain, "deep_scan": True}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["domain"] == sample_merchant_domain
    assert "risk_score" in data
    assert "risk_level" in data
    assert "decision" in data
    assert "confidence" in data
    assert "signals" in data


def test_analyze_merchant_new(client):
    """Test analyzing new merchant domain"""
    response = client.post(
        "/api/v1/merchants/analyze",
        json={"domain": "new-merchant-test.com", "deep_scan": True}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["domain"] == "new-merchant-test.com"
    assert 0 <= data["risk_score"] <= 100
    assert data["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_analyze_merchant_invalid_domain(client):
    """Test analyzing with invalid domain"""
    response = client.post(
        "/api/v1/merchants/analyze",
        json={"domain": "", "deep_scan": True}
    )
    assert response.status_code == 422  # Validation error


def test_merchant_risk_score_range(client):
    """Test that merchant risk scores are in valid range"""
    response = client.get("/api/v1/merchants")
    assert response.status_code == 200
    
    data = response.json()
    for merchant in data["merchants"]:
        assert 0 <= merchant["risk_score"] <= 100
        assert merchant["confidence"] >= 0
