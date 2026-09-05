"""
Tests for Evidence API Endpoints
"""

import pytest


def test_get_signals(client):
    """Test getting all signals"""
    response = client.get("/api/v1/evidence/signals")
    assert response.status_code == 200
    
    data = response.json()
    assert "signals" in data
    assert "categories" in data
    assert "total_count" in data
    assert len(data["signals"]) > 0


def test_get_signals_by_category(client):
    """Test filtering signals by category"""
    response = client.get("/api/v1/evidence/signals?category=WEBSITE")
    assert response.status_code == 200
    
    data = response.json()
    for signal in data["signals"]:
        assert signal["category"] == "WEBSITE"


def test_get_signal_by_id(client):
    """Test getting specific signal"""
    # First get all signals
    response = client.get("/api/v1/evidence/signals")
    signal_id = response.json()["signals"][0]["id"]
    
    # Get that specific signal
    response = client.get(f"/api/v1/evidence/signals/{signal_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == signal_id
    assert "category" in data
    assert "title" in data
    assert "impact" in data


def test_get_signal_not_found(client):
    """Test getting non-existent signal"""
    response = client.get("/api/v1/evidence/signals/invalid_signal_id")
    assert response.status_code == 404


def test_get_categories(client):
    """Test getting signal categories"""
    response = client.get("/api/v1/evidence/categories")
    assert response.status_code == 200
    
    data = response.json()
    assert "categories" in data
    assert "total_categories" in data
    
    # Validate category structure
    for category in data["categories"]:
        assert "name" in category
        assert "description" in category
        assert "signal_count" in category


def test_get_impact_analysis(client):
    """Test impact analysis endpoint"""
    response = client.get("/api/v1/evidence/impact-analysis")
    assert response.status_code == 200
    
    data = response.json()
    assert "impact_distribution" in data
    assert "high_impact_signals" in data
    assert "total_signals" in data
    
    # Validate impact distribution
    assert "HIGH" in data["impact_distribution"]
    assert "MEDIUM" in data["impact_distribution"]
    assert "LOW" in data["impact_distribution"]


def test_get_provenance_info(client):
    """Test provenance information endpoint"""
    response = client.get("/api/v1/evidence/provenance")
    assert response.status_code == 200
    
    data = response.json()
    assert "provenances" in data
    assert "total_sources" in data
    
    # Validate provenance structure
    for prov in data["provenances"]:
        assert "name" in prov
        assert "description" in prov
        assert "signal_count" in prov
        assert "signals" in prov


def test_signal_structure(client):
    """Test that signals have proper structure"""
    response = client.get("/api/v1/evidence/signals")
    assert response.status_code == 200
    
    data = response.json()
    for signal in data["signals"]:
        assert "id" in signal
        assert "category" in signal
        assert "title" in signal
        assert "value" in signal
        assert "impact" in signal
        assert "confidence" in signal
        assert "provenance" in signal
        assert "description" in signal
        
        # Validate confidence range
        assert 0 <= signal["confidence"] <= 100
