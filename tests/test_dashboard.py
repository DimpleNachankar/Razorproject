"""
Tests for Dashboard API Endpoints
"""

import pytest


def test_get_dashboard_overview(client):
    """Test dashboard overview endpoint"""
    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_transactions" in data
    assert "total_volume_inr" in data
    assert "flagged_transactions" in data
    assert "flagged_percentage" in data
    assert "high_risk_merchants" in data
    assert "manual_review_rate" in data
    assert "timestamp" in data
    
    # Validate data types
    assert isinstance(data["total_transactions"], int)
    assert isinstance(data["total_volume_inr"], (int, float))
    assert data["total_transactions"] > 0


def test_get_system_health(client):
    """Test system health endpoint"""
    response = client.get("/api/v1/dashboard/system-health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["engine_status"] == "active"
    assert data["demo_mode"] == True
    assert "processing_metrics" in data
    assert "error_rates" in data
    assert "uptime" in data


def test_processing_metrics(client):
    """Test processing metrics structure"""
    response = client.get("/api/v1/dashboard/system-health")
    assert response.status_code == 200
    
    data = response.json()
    metrics = data["processing_metrics"]
    
    assert "avg_merchant_analysis_ms" in metrics
    assert "avg_transaction_eval_ms" in metrics
    assert "p95_latency_ms" in metrics
    assert "p99_latency_ms" in metrics
    
    # Validate latency values are reasonable
    assert metrics["avg_merchant_analysis_ms"] > 0
    assert metrics["p99_latency_ms"] > metrics["p95_latency_ms"]


def test_get_activity_feed(client):
    """Test activity feed endpoint"""
    response = client.get("/api/v1/dashboard/activity-feed?limit=10")
    assert response.status_code == 200
    
    data = response.json()
    assert "activities" in data
    assert "total" in data
    assert "timestamp" in data
    assert len(data["activities"]) <= 10


def test_activity_feed_structure(client):
    """Test activity feed item structure"""
    response = client.get("/api/v1/dashboard/activity-feed?limit=5")
    assert response.status_code == 200
    
    data = response.json()
    for activity in data["activities"]:
        assert "id" in activity
        assert "type" in activity
        assert "severity" in activity
        assert "title" in activity
        assert "description" in activity
        assert "risk_score" in activity
        assert "decision" in activity
        assert "timestamp" in activity


def test_get_alerts(client):
    """Test alerts endpoint"""
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    
    data = response.json()
    assert "alerts" in data
    assert "total_active" in data
    assert "last_checked" in data
    assert isinstance(data["alerts"], list)


def test_alert_structure(client):
    """Test alert structure when alerts exist"""
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    
    data = response.json()
    if data["total_active"] > 0:
        for alert in data["alerts"]:
            assert "id" in alert
            assert "type" in alert
            assert "severity" in alert
            assert "title" in alert
            assert "description" in alert
            assert "recommendation" in alert
            assert "timestamp" in alert


def test_get_quick_stats(client):
    """Test quick stats endpoint"""
    response = client.get("/api/v1/dashboard/quick-stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "transactions" in data
    assert "merchants" in data
    assert "risk_distribution" in data
    assert "timestamp" in data


def test_quick_stats_transactions(client):
    """Test quick stats transaction data"""
    response = client.get("/api/v1/dashboard/quick-stats")
    assert response.status_code == 200
    
    data = response.json()
    txn_stats = data["transactions"]
    
    assert "total" in txn_stats
    assert "total_volume_inr" in txn_stats
    assert "average_amount" in txn_stats
    assert "blocked" in txn_stats
    assert "review_required" in txn_stats


def test_quick_stats_merchants(client):
    """Test quick stats merchant data"""
    response = client.get("/api/v1/dashboard/quick-stats")
    assert response.status_code == 200
    
    data = response.json()
    merchant_stats = data["merchants"]
    
    assert "total" in merchant_stats
    assert "low_risk" in merchant_stats
    assert "medium_risk" in merchant_stats
    assert "high_risk" in merchant_stats
    
    # Validate sum
    total = merchant_stats["low_risk"] + merchant_stats["medium_risk"] + merchant_stats["high_risk"]
    assert total == merchant_stats["total"]
