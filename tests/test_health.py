"""
Tests for Health Check Endpoints
"""

import pytest


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert data["demo_mode"] == True
    assert "version" in data


def test_ping(client):
    """Test ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert data["message"] == "pong"


def test_root_redirect(client):
    """Test root redirects to docs"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_api_info(client):
    """Test API info endpoint"""
    response = client.get("/api/info")
    assert response.status_code == 200
    
    data = response.json()
    assert "api" in data
    assert "endpoints" in data
    assert "features" in data
    assert data["api"]["demo_mode"] == True


def test_system_status(client):
    """Test system status endpoint"""
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "operational"
    assert "engine" in data
    assert "statistics" in data
    assert "configuration" in data
