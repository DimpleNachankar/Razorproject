"""
Tests for Risk Engine
"""

import pytest
from app.risk_engine import (
    analyze_merchant_risk,
    evaluate_transaction_risk,
    calculate_simulator_risk,
    estimate_domain_age
)
from app.schemas import PaymentMethod, RiskLevel


def test_analyze_merchant_risk_low():
    """Test merchant risk analysis for low-risk merchant"""
    risk_score, risk_level, decision, confidence, signals = analyze_merchant_risk(
        domain="example.com",
        age_days=730,
        has_ssl=True,
        has_refund_policy=True,
        contact_quality="Complete"
    )
    
    assert 0 <= risk_score <= 100
    assert risk_level == RiskLevel.LOW
    assert decision.value == "ALLOW"
    assert confidence > 0
    assert len(signals) > 0


def test_analyze_merchant_risk_high():
    """Test merchant risk analysis for high-risk merchant"""
    risk_score, risk_level, decision, confidence, signals = analyze_merchant_risk(
        domain="suspicious-site.xyz",
        age_days=7,
        has_ssl=False,
        has_refund_policy=False,
        contact_quality="Missing"
    )
    
    assert risk_score > 50
    assert risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]
    assert len(signals) > 0


def test_evaluate_transaction_risk_low():
    """Test transaction risk evaluation for low-risk transaction"""
    risk_score, risk_level, decision, confidence, signals = evaluate_transaction_risk(
        amount=1000.0,
        payment_method=PaymentMethod.UPI,
        merchant_risk_score=15.0,
        velocity_1h=1,
        failed_attempts_15m=0,
        customer_account_age_days=365
    )
    
    assert 0 <= risk_score <= 100
    assert risk_level == RiskLevel.LOW
    assert decision.value == "ALLOW"
    assert len(signals) > 0


def test_evaluate_transaction_risk_high():
    """Test transaction risk evaluation for high-risk transaction"""
    risk_score, risk_level, decision, confidence, signals = evaluate_transaction_risk(
        amount=100000.0,
        payment_method=PaymentMethod.CARD,
        merchant_risk_score=80.0,
        velocity_1h=15,
        failed_attempts_15m=5,
        customer_account_age_days=1
    )
    
    assert risk_score > 60
    assert risk_level == RiskLevel.HIGH
    assert decision.value in ["REQUIRE_REVIEW", "BLOCK_DEMO_PAYMENT"]
    assert len(signals) > 0


def test_calculate_simulator_risk():
    """Test simulator risk calculation"""
    result = calculate_simulator_risk(
        amount=5000.0,
        payment_method=PaymentMethod.CARD,
        velocity_1h=2,
        failed_attempts_15m=0,
        merchant_risk_level=RiskLevel.LOW,
        customer_account_age_days=365
    )
    
    assert "risk_score" in result
    assert "risk_level" in result
    assert "decision" in result
    assert "confidence" in result
    assert "contributing_factors" in result
    assert "calculation_breakdown" in result
    
    assert 0 <= result["risk_score"] <= 100
    assert isinstance(result["contributing_factors"], list)
    assert isinstance(result["calculation_breakdown"], dict)


def test_estimate_domain_age():
    """Test domain age estimation"""
    # Standard .com domain
    age = estimate_domain_age("example.com")
    assert age > 0
    
    # Suspicious TLD
    age = estimate_domain_age("suspicious.xyz")
    assert age <= 21
    
    # Indian domain
    age = estimate_domain_age("example.in")
    assert age >= 365


def test_risk_score_boundaries():
    """Test that risk scores stay within 0-100 range"""
    # Extreme low risk
    risk_score, _, _, _, _ = analyze_merchant_risk(
        domain="trusted.com",
        age_days=3650,
        has_ssl=True,
        has_refund_policy=True,
        contact_quality="Complete"
    )
    assert 0 <= risk_score <= 100
    
    # Extreme high risk
    risk_score, _, _, _, _ = analyze_merchant_risk(
        domain="bad.xyz",
        age_days=1,
        has_ssl=False,
        has_refund_policy=False,
        contact_quality="Missing"
    )
    assert 0 <= risk_score <= 100


def test_signal_generation():
    """Test that signals are generated properly"""
    _, _, _, _, signals = analyze_merchant_risk(
        domain="test.com",
        age_days=100,
        has_ssl=True,
        has_refund_policy=True,
        contact_quality="Partial"
    )
    
    # Verify signal structure
    for signal in signals:
        assert hasattr(signal, 'id')
        assert hasattr(signal, 'category')
        assert hasattr(signal, 'title')
        assert hasattr(signal, 'value')
        assert hasattr(signal, 'impact')
        assert hasattr(signal, 'confidence')
        assert hasattr(signal, 'provenance')
        assert hasattr(signal, 'description')
        assert 0 <= signal.confidence <= 100


def test_payment_method_risk_profiles():
    """Test different payment method risk profiles"""
    base_params = {
        "amount": 5000.0,
        "merchant_risk_score": 20.0,
        "velocity_1h": 1,
        "failed_attempts_15m": 0,
        "customer_account_age_days": 365
    }
    
    # Card payment
    card_score, _, _, _, _ = evaluate_transaction_risk(
        **base_params,
        payment_method=PaymentMethod.CARD
    )
    
    # UPI payment
    upi_score, _, _, _, _ = evaluate_transaction_risk(
        **base_params,
        payment_method=PaymentMethod.UPI
    )
    
    # Card should have slightly higher risk than UPI
    assert card_score >= upi_score
