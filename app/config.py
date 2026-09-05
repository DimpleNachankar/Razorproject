"""
Configuration and Settings for TRUSTSHIELD API
Environment variables, constants, and application settings
"""

from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    Falls back to sensible defaults for demo mode
    """
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Metadata
    API_VERSION: str = "v1"
    API_TITLE: str = "TRUSTSHIELD Risk Intelligence API"
    API_DESCRIPTION: str = """
    **TRUSTSHIELD** - AI-Powered Merchant & Real-Time Payment Risk Intelligence Platform
    
    Built for Razorpay AI Buildathon 2026.
    
    ## Features
    
    - **Merchant Risk Assessment**: Domain analysis, identity verification, policy detection
    - **Transaction Monitoring**: Real-time payment risk evaluation with velocity tracking
    - **Evidence-Based Decisions**: Structured signal catalog with provenance tracking
    - **Risk Scoring**: 0-100 risk score with confidence levels
    - **Actionable Recommendations**: ALLOW, MONITOR, REQUIRE_REVIEW, BLOCK_DEMO_PAYMENT
    
    ## Demo Mode
    
    This API operates in **DEMO MODE** with:
    - ✅ Mock merchant and transaction data
    - ✅ Deterministic risk calculation
    - ✅ No external API calls
    - ✅ No real payment processing
    
    ## Architecture
    
    TRUSTSHIELD is a **complementary risk intelligence layer** that enriches Razorpay's 
    core fraud detection with merchant website signals, entity provenance, and transaction 
    velocity indicators.
    
    **NOT A REPLACEMENT** for existing fraud systems.
    """
    
    # CORS Configuration
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000"
    
    # Demo Mode
    DEMO_MODE: bool = True
    VERBOSE_LOGGING: bool = True
    
    # Risk Thresholds (0-100 scale)
    AUTO_ALLOW_THRESHOLD: int = 30
    REQUIRE_REVIEW_THRESHOLD: int = 60
    AUTO_BLOCK_THRESHOLD: int = 85
    
    # Rate Limiting (future use)
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # API Configuration
    MAX_PAGE_SIZE: int = 100
    DEFAULT_PAGE_SIZE: int = 20
    
    # Processing Timeouts
    MERCHANT_ANALYSIS_TIMEOUT_MS: int = 500
    TRANSACTION_EVAL_TIMEOUT_MS: int = 100
    
    # Mock Data Configuration
    MOCK_MERCHANT_COUNT: int = 50
    MOCK_TRANSACTION_COUNT: int = 200
    
    # Security (for future use)
    SECRET_KEY: str = "demo-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse ALLOWED_ORIGINS into a list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def api_prefix(self) -> str:
        """API route prefix"""
        return f"/api/{self.API_VERSION}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# ============================================================================
# CONSTANTS
# ============================================================================

class RiskThresholds:
    """Risk score threshold constants"""
    LOW_MAX = 30
    MEDIUM_MAX = 60
    HIGH_MAX = 84
    CRITICAL_MIN = 85


class SignalWeights:
    """Signal impact weights for risk calculation"""
    
    # Merchant Signals
    DOMAIN_AGE_NEW = 25  # < 30 days
    DOMAIN_AGE_MEDIUM = 15  # < 180 days
    NO_SSL = 20
    NO_REFUND_POLICY = 15
    INCOMPLETE_CONTACT = 12
    SUSPICIOUS_CONTENT = 30
    
    # Transaction Signals
    HIGH_AMOUNT = 15  # > 50k INR
    HIGH_VELOCITY = 25  # > 5 txns/hour
    FAILED_ATTEMPTS = 20  # > 2 failures
    NEW_CUSTOMER = 10  # < 30 days account
    MISMATCH_LOCATION = 18
    
    # Payment Method Risk
    CARD_RISK_BASE = 5
    UPI_RISK_BASE = 3
    NETBANKING_RISK_BASE = 2


class BusinessCategories:
    """Common business category classifications"""
    HANDICRAFTS = "Handicrafts & Home Decor"
    ELECTRONICS = "Electronics & Gadgets"
    FASHION = "Fashion & Apparel"
    GROCERIES = "Groceries & Essentials"
    BOOKS = "Books & Stationery"
    JEWELRY = "Jewelry & Accessories"
    PHARMACEUTICALS = "Pharmaceuticals & Healthcare"
    SERVICES = "Services & Subscriptions"
    TRAVEL = "Travel & Hospitality"
    EDUCATION = "Education & E-Learning"


class PaymentMethodRiskProfiles:
    """Risk profiles for different payment methods"""
    
    CARD = {
        "base_risk": 5,
        "chargeback_rate": 0.8,
        "fraud_vulnerability": "MEDIUM",
        "verification_required": True
    }
    
    UPI = {
        "base_risk": 3,
        "chargeback_rate": 0.2,
        "fraud_vulnerability": "LOW",
        "verification_required": True
    }
    
    NETBANKING = {
        "base_risk": 2,
        "chargeback_rate": 0.1,
        "fraud_vulnerability": "LOW",
        "verification_required": True
    }


class ErrorCodes:
    """Application error codes"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    MERCHANT_NOT_FOUND = "MERCHANT_NOT_FOUND"
    TRANSACTION_NOT_FOUND = "TRANSACTION_NOT_FOUND"
    SIGNAL_NOT_FOUND = "SIGNAL_NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INVALID_DOMAIN = "INVALID_DOMAIN"
    ANALYSIS_TIMEOUT = "ANALYSIS_TIMEOUT"


class ResponseMessages:
    """Standard response messages"""
    MERCHANT_ANALYZED = "Merchant analysis completed successfully"
    TRANSACTION_EVALUATED = "Transaction risk evaluated successfully"
    CHECKOUT_EVALUATED = "Checkout risk evaluation completed"
    SIMULATOR_CALCULATED = "Risk score calculated successfully"
    DATA_RETRIEVED = "Data retrieved successfully"
    NOT_FOUND = "Resource not found"
    INVALID_REQUEST = "Invalid request parameters"
    INTERNAL_ERROR = "Internal server error occurred"
    DEMO_MODE_ACTIVE = "Demo mode active - using mock data"


class LogMessages:
    """Logging message templates"""
    REQUEST_RECEIVED = "Request received: {method} {path}"
    REQUEST_COMPLETED = "Request completed: {method} {path} - {status_code} ({duration}ms)"
    MERCHANT_ANALYSIS = "Analyzing merchant: {domain}"
    TRANSACTION_EVAL = "Evaluating transaction: {transaction_id}"
    RISK_CALCULATED = "Risk calculated: score={score}, level={level}, decision={decision}"
    ERROR_OCCURRED = "Error occurred: {error_type} - {message}"


# ============================================================================
# SINGLETON SETTINGS INSTANCE
# ============================================================================

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Uses lru_cache to ensure settings are loaded only once
    """
    return Settings()


# ============================================================================
# DEMO PRESETS
# ============================================================================

class DemoPresets:
    """Predefined demo scenarios for quick testing"""
    
    LEGIT_MERCHANT = {
        "name": "Legit: UrbanNest Handicrafts",
        "domain": "urbannest.in",
        "expected_risk": "LOW",
        "expected_score": 18
    }
    
    SUSPICIOUS_MERCHANT = {
        "name": "Suspicious: SwiftDrop Electronics",
        "domain": "swiftdrop-deals.shop",
        "expected_risk": "HIGH",
        "expected_score": 87
    }
    
    MEDIUM_MERCHANT = {
        "name": "Needs Review: TechMart Gadgets",
        "domain": "techmart-india.com",
        "expected_risk": "MEDIUM",
        "expected_score": 54
    }
    
    NORMAL_TRANSACTION = {
        "amount": 2499.00,
        "payment_method": "CARD",
        "velocity_1h": 1,
        "failed_attempts_15m": 0,
        "expected_risk": "LOW"
    }
    
    HIGH_VELOCITY_ATTACK = {
        "amount": 15000.00,
        "payment_method": "CARD",
        "velocity_1h": 12,
        "failed_attempts_15m": 3,
        "expected_risk": "HIGH"
    }
    
    HIGH_VALUE_FIRST_TIME = {
        "amount": 89000.00,
        "payment_method": "CARD",
        "velocity_1h": 1,
        "failed_attempts_15m": 0,
        "customer_account_age_days": 2,
        "expected_risk": "HIGH"
    }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_risk_level_from_score(score: float) -> str:
    """
    Determine risk level from score
    
    Args:
        score: Risk score (0-100)
        
    Returns:
        Risk level: LOW, MEDIUM, or HIGH
    """
    if score <= RiskThresholds.LOW_MAX:
        return "LOW"
    elif score <= RiskThresholds.MEDIUM_MAX:
        return "MEDIUM"
    else:
        return "HIGH"


def get_decision_from_score(score: float) -> str:
    """
    Determine recommended decision from risk score
    
    Args:
        score: Risk score (0-100)
        
    Returns:
        Decision: ALLOW, MONITOR, REQUIRE_REVIEW, or BLOCK_DEMO_PAYMENT
    """
    settings = get_settings()
    
    if score < settings.AUTO_ALLOW_THRESHOLD:
        return "ALLOW"
    elif score < settings.REQUIRE_REVIEW_THRESHOLD:
        return "MONITOR"
    elif score < settings.AUTO_BLOCK_THRESHOLD:
        return "REQUIRE_REVIEW"
    else:
        return "BLOCK_DEMO_PAYMENT"


def calculate_confidence_score(signal_count: int, signal_conflicts: int = 0) -> float:
    """
    Calculate confidence score based on signal quality
    
    Args:
        signal_count: Number of signals collected
        signal_conflicts: Number of conflicting signals
        
    Returns:
        Confidence percentage (0-100)
    """
    base_confidence = min(60 + (signal_count * 5), 95)
    conflict_penalty = signal_conflicts * 10
    confidence = max(base_confidence - conflict_penalty, 30)
    
    return round(confidence, 1)


def format_currency_inr(amount: float) -> str:
    """
    Format amount in Indian currency format
    
    Args:
        amount: Amount in INR
        
    Returns:
        Formatted string (e.g., "₹2,499.00")
    """
    return f"₹{amount:,.2f}"


def get_api_tags() -> List[dict]:
    """
    Get OpenAPI tags for documentation
    
    Returns:
        List of tag dictionaries
    """
    return [
        {
            "name": "Health",
            "description": "API health check and status endpoints"
        },
        {
            "name": "Dashboard",
            "description": "Dashboard overview and system metrics"
        },
        {
            "name": "Merchants",
            "description": "Merchant risk analysis and intelligence"
        },
        {
            "name": "Transactions",
            "description": "Transaction monitoring and risk evaluation"
        },
        {
            "name": "Checkout",
            "description": "Real-time checkout risk evaluation"
        },
        {
            "name": "Simulator",
            "description": "Interactive risk calculation simulator"
        },
        {
            "name": "Evidence",
            "description": "Evidence signals and forensic investigation"
        },
        {
            "name": "Analytics",
            "description": "Analytics, trends, and operational insights"
        },
        {
            "name": "Models",
            "description": "ML model status and performance specifications"
        }
    ]


# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

__all__ = [
    "Settings",
    "get_settings",
    "RiskThresholds",
    "SignalWeights",
    "BusinessCategories",
    "PaymentMethodRiskProfiles",
    "ErrorCodes",
    "ResponseMessages",
    "LogMessages",
    "DemoPresets",
    "get_risk_level_from_score",
    "get_decision_from_score",
    "calculate_confidence_score",
    "format_currency_inr",
    "get_api_tags"
]
