"""
Tests for Analytics API Endpoints
"""

import pytest


def test_get_analytics_overview(client):
    """Test analytics overview endpoint"""
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    
    data = response.json()
    assert "risk_distribution" in data
    assert "transaction_volume_24h" in data
    assert "flagged_volume_24h" in data
    assert "decision_distribution" in data
    assert "payment_method_breakdown" in data


def test_risk_distribution(client):
    """Test risk distribution data"""
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    
    data = response.json()
    risk_dist = data["risk_distribution"]
    
    assert "low" in risk_dist
    assert "medium" in risk_dist
    assert "high" in risk_dist
    assert all(isinstance(v, int) for v in risk_dist.values())


def test_get_risk_trends(client):
    """Test risk trends endpoint"""
    response = client.get("/api/v1/analytics/trends?timeframe=24h")
    assert response.status_code == 200
    
    data = response.json()
    assert "timeframe" in data
    assert "trends" in data
    assert "summary" in data
    
    # Validate trend structure
    for trend in data["trends"]:
        assert "timestamp" in trend
        assert "average_risk_score" in trend
        assert "transaction_count" in trend


def test_get_merchant_risk_distribution(client):
    """Test merchant risk distribution"""
    response = client.get("/api/v1/analytics/merchant-risk-distribution")
    assert response.status_code == 200
    
    data = response.json()
    assert "risk_distribution" in data
    assert "total_merchants" in data
    assert "category_analysis" in data
    assert "high_risk_merchants" in data


def test_get_payment_method_analysis(client):
    """Test payment method analysis"""
    response = client.get("/api/v1/analytics/payment-method-analysis")
    assert response.status_code == 200
    
    data = response.json()
    assert "payment_methods" in data
    assert "total_transactions" in data
    
    # Validate payment method data
    for method, analysis in data["payment_methods"].items():
        assert "count" in analysis
        assert "avg_amount" in analysis
        assert "avg_risk_score" in analysis
        assert "high_risk_rate" in analysis


def test_get_velocity_patterns(client):
    """Test velocity pattern analysis"""
    response = client.get("/api/v1/analytics/velocity-patterns")
    assert response.status_code == 200
    
    data = response.json()
    assert "velocity_analysis" in data
    assert "total_transactions" in data
    
    # Validate velocity groups
    velocity_analysis = data["velocity_analysis"]
    assert "normal" in velocity_analysis
    assert "elevated" in velocity_analysis
    assert "high" in velocity_analysis
    assert "suspicious" in velocity_analysis


def test_time_series_structure(client):
    """Test time series data structure"""
    response = client.get("/api/v1/analytics/overview")
    assert response.status_code == 200
    
    data = response.json()
    
    # Validate time series structure
    for point in data["transaction_volume_24h"]:
        assert "timestamp" in point
        assert "value" in point
        assert isinstance(point["value"], (int, float))


def test_analytics_with_different_timeframes(client):
    """Test analytics with different timeframes"""
    timeframes = ["24h", "7d", "30d"]
    
    for timeframe in timeframes:
        response = client.get(f"/api/v1/analytics/trends?timeframe={timeframe}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["timeframe"] == timeframe
