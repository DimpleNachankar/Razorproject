"""
Tests for Models API Endpoints
"""

import pytest


def test_get_model_status(client):
    """Test model status endpoint"""
    response = client.get("/api/v1/models/status")
    assert response.status_code == 200
    
    data = response.json()
    assert "models" in data
    assert "demo_mode" in data
    assert "note" in data
    assert data["demo_mode"] == True
    
    # Validate model structure
    for model in data["models"]:
        assert "model_name" in model
        assert "model_type" in model
        assert "status" in model
        assert "version" in model
        assert "target_latency_ms" in model
        assert "description" in model


def test_get_model_architecture(client):
    """Test model architecture endpoint"""
    response = client.get("/api/v1/models/architecture")
    assert response.status_code == 200
    
    data = response.json()
    assert "architecture" in data
    assert "feature_importance" in data
    assert "training_requirements" in data
    assert "performance_targets" in data


def test_architecture_pipeline(client):
    """Test architecture pipeline structure"""
    response = client.get("/api/v1/models/architecture")
    assert response.status_code == 200
    
    data = response.json()
    pipeline = data["architecture"]["pipeline"]
    
    assert len(pipeline) > 0
    for stage in pipeline:
        assert "stage" in stage
        assert "description" in stage
        assert "components" in stage


def test_get_model_evaluation(client):
    """Test model evaluation endpoint"""
    response = client.get("/api/v1/models/evaluation")
    assert response.status_code == 200
    
    data = response.json()
    assert "evaluation_methodology" in data
    assert "metrics" in data
    assert "confusion_matrix_example" in data
    assert "monitoring" in data


def test_evaluation_metrics(client):
    """Test evaluation metrics structure"""
    response = client.get("/api/v1/models/evaluation")
    assert response.status_code == 200
    
    data = response.json()
    metrics = data["metrics"]
    
    assert "primary" in metrics
    assert "secondary" in metrics
    assert "operational" in metrics
    
    # Validate primary metrics
    for metric in metrics["primary"]:
        assert "name" in metric
        assert "description" in metric
        assert "target" in metric


def test_get_feature_importance(client):
    """Test feature importance endpoint"""
    response = client.get("/api/v1/models/feature-importance")
    assert response.status_code == 200
    
    data = response.json()
    assert "merchant_model" in data
    assert "transaction_model" in data
    
    # Validate feature structure
    for feature in data["merchant_model"]:
        assert "feature" in feature
        assert "importance" in feature
        assert "description" in feature
        assert 0 <= feature["importance"] <= 1


def test_model_types(client):
    """Test that expected model types are present"""
    response = client.get("/api/v1/models/status")
    assert response.status_code == 200
    
    data = response.json()
    model_names = [m["model_name"] for m in data["models"]]
    
    assert "merchant_risk_classifier" in model_names
    assert "transaction_anomaly_detector" in model_names


def test_performance_targets(client):
    """Test performance targets structure"""
    response = client.get("/api/v1/models/architecture")
    assert response.status_code == 200
    
    data = response.json()
    targets = data["performance_targets"]
    
    assert "merchant_classifier" in targets
    assert "transaction_detector" in targets
    assert "latency" in targets
