"""
Pytest Configuration and Fixtures
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Create test client for FastAPI application
    """
    return TestClient(app)


@pytest.fixture
def sample_merchant_domain():
    """
    Sample merchant domain for testing
    """
    return "urbannest.in"


@pytest.fixture
def sample_merchant_analysis_request():
    """
    Sample merchant analysis request payload
    """
    return {
        "domain": "test-merchant.com",
        "deep_scan": True
    }


@pytest.fixture
def sample_checkout_request():
    """
    Sample checkout evaluation request payload
    """
    return {
        "merchant_id": "merch_001",
        "amount": 2499.00,
        "payment_method": "CARD",
        "card_last4": "4242",
        "customer_email": "test@example.com",
        "ip_address": "106.51.75.142",
        "device_fingerprint": "fp_test123"
    }


@pytest.fixture
def sample_simulator_request():
    """
    Sample risk simulator request payload
    """
    return {
        "amount": 5000.0,
        "payment_method": "CARD",
        "velocity_1h": 2,
        "failed_attempts_15m": 0,
        "merchant_risk_level": "LOW",
        "customer_account_age_days": 365
    }
