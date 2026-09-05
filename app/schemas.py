"""
Pydantic Schemas for TRUSTSHIELD API
All data models for requests, responses, and internal representations
"""

from typing import Literal, Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, validator
from enum import Enum


# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class RiskLevel(str, Enum):
    """Risk severity classification"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class RiskDecision(str, Enum):
    """Risk-based action recommendation"""
    ALLOW = "ALLOW"
    MONITOR = "MONITOR"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"
    BLOCK_DEMO_PAYMENT = "BLOCK_DEMO_PAYMENT"
    BLOCK = "BLOCK"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"


class SignalCategory(str, Enum):
    """Evidence signal categorization"""
    WEBSITE = "WEBSITE"
    IDENTITY = "IDENTITY"
    VELOCITY = "VELOCITY"
    PAYMENT = "PAYMENT"
    NETWORK = "NETWORK"


class SignalProvenance(str, Enum):
    """Source of evidence signal"""
    DNS_SCAN = "DNS_SCAN"
    CONTENT_EVAL = "CONTENT_EVAL"
    PAYMENT_GATEWAY = "PAYMENT_GATEWAY"
    CONSORTIUM_MOCK = "CONSORTIUM_MOCK"
    VELOCITY_TRACKER = "VELOCITY_TRACKER"
    DEVICE_FINGERPRINT = "DEVICE_FINGERPRINT"


class PaymentMethod(str, Enum):
    """Payment method types"""
    CARD = "CARD"
    UPI = "UPI"
    NETBANKING = "NETBANKING"


class ImpactLevel(str, Enum):
    """Signal impact on risk score"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


# ============================================================================
# EVIDENCE SIGNAL MODELS
# ============================================================================

class EvidenceSignal(BaseModel):
    """Individual evidence signal with confidence and provenance"""
    id: str = Field(..., description="Unique signal identifier")
    category: SignalCategory = Field(..., description="Signal category")
    title: str = Field(..., description="Human-readable signal title")
    value: str = Field(..., description="Signal value or finding")
    impact: ImpactLevel = Field(..., description="Impact on risk assessment")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    provenance: SignalProvenance = Field(..., description="Source of signal")
    description: str = Field(..., description="Detailed explanation")
    timestamp: Optional[datetime] = Field(default=None, description="When signal was detected")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "sig_domain_age_001",
                "category": "WEBSITE",
                "title": "Domain Age",
                "value": "14 days",
                "impact": "HIGH",
                "confidence": 95.0,
                "provenance": "DNS_SCAN",
                "description": "Domain registered recently, elevated fraud risk",
                "timestamp": "2026-09-03T10:30:00Z"
            }
        }


# ============================================================================
# MERCHANT MODELS
# ============================================================================

class MerchantRecord(BaseModel):
    """Complete merchant risk assessment record"""
    id: str = Field(..., description="Unique merchant identifier")
    name: str = Field(..., description="Merchant business name")
    domain: str = Field(..., description="Merchant website domain")
    category: str = Field(..., description="Business category")
    age_days: int = Field(..., ge=0, description="Domain age in days")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    decision: RiskDecision = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    signals: List[EvidenceSignal] = Field(default_factory=list, description="Evidence signals")
    refund_policy_detected: bool = Field(default=False, description="Refund policy found")
    contact_score: str = Field(..., description="Contact information quality")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Record creation time")
    last_evaluated: datetime = Field(default_factory=datetime.utcnow, description="Last evaluation time")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "merch_001",
                "name": "UrbanNest Handicrafts",
                "domain": "urbannest.in",
                "category": "Handicrafts & Home Decor",
                "age_days": 730,
                "risk_score": 18.0,
                "risk_level": "LOW",
                "decision": "ALLOW",
                "confidence": 92.0,
                "signals": [],
                "refund_policy_detected": True,
                "contact_score": "Complete",
                "created_at": "2026-09-01T00:00:00Z",
                "last_evaluated": "2026-09-03T10:30:00Z"
            }
        }


class MerchantAnalysisRequest(BaseModel):
    """Request to analyze a merchant domain"""
    domain: str = Field(..., description="Merchant domain to analyze", min_length=3, max_length=255)
    deep_scan: bool = Field(default=True, description="Perform deep signal analysis")

    @validator('domain')
    def validate_domain(cls, v):
        """Clean and validate domain"""
        # Remove protocol and trailing slashes
        v = v.replace('https://', '').replace('http://', '').strip('/')
        if ' ' in v:
            raise ValueError('Domain cannot contain spaces')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "domain": "urbannest.in",
                "deep_scan": True
            }
        }


class MerchantListResponse(BaseModel):
    """Paginated merchant list response"""
    merchants: List[MerchantRecord] = Field(..., description="List of merchants")
    total: int = Field(..., description="Total merchant count")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")

    class Config:
        json_schema_extra = {
            "example": {
                "merchants": [],
                "total": 42,
                "page": 1,
                "page_size": 20
            }
        }


# ============================================================================
# TRANSACTION MODELS
# ============================================================================

class TransactionRecord(BaseModel):
    """Complete transaction risk assessment record"""
    id: str = Field(..., description="Unique transaction identifier")
    merchant_id: str = Field(..., description="Associated merchant ID")
    merchant_name: str = Field(..., description="Merchant business name")
    amount: float = Field(..., gt=0, description="Transaction amount")
    currency: str = Field(default="INR", description="Currency code")
    method: PaymentMethod = Field(..., description="Payment method used")
    card_last4: Optional[str] = Field(None, description="Last 4 digits of card", min_length=4, max_length=4)
    upi_handle: Optional[str] = Field(None, description="UPI handle if applicable")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    decision: RiskDecision = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    velocity_1h: int = Field(default=1, ge=0, description="Transactions in last hour")
    ip_location: str = Field(..., description="IP geolocation")
    device_fingerprint: Optional[str] = Field(None, description="Device identifier hash")
    signals: List[EvidenceSignal] = Field(default_factory=list, description="Evidence signals")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Transaction timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "txn_20260903_001",
                "merchant_id": "merch_001",
                "merchant_name": "UrbanNest Handicrafts",
                "amount": 2499.00,
                "currency": "INR",
                "method": "CARD",
                "card_last4": "4242",
                "risk_score": 22.0,
                "risk_level": "LOW",
                "decision": "ALLOW",
                "confidence": 88.0,
                "velocity_1h": 1,
                "ip_location": "Mumbai, Maharashtra",
                "device_fingerprint": "fp_abc123xyz",
                "signals": [],
                "timestamp": "2026-09-03T10:30:00Z"
            }
        }


class TransactionListResponse(BaseModel):
    """Paginated transaction list response"""
    transactions: List[TransactionRecord] = Field(..., description="List of transactions")
    total: int = Field(..., description="Total transaction count")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")

    class Config:
        json_schema_extra = {
            "example": {
                "transactions": [],
                "total": 14290,
                "page": 1,
                "page_size": 50
            }
        }


# ============================================================================
# CHECKOUT & SIMULATOR MODELS
# ============================================================================

class CheckoutEvaluationRequest(BaseModel):
    """Request to evaluate checkout risk in real-time"""
    merchant_id: str = Field(..., description="Merchant identifier")
    amount: float = Field(..., gt=0, le=1000000, description="Transaction amount in INR")
    payment_method: PaymentMethod = Field(..., description="Selected payment method")
    card_last4: Optional[str] = Field(None, description="Last 4 digits of card")
    upi_handle: Optional[str] = Field(None, description="UPI handle")
    customer_email: Optional[str] = Field(None, description="Customer email")
    ip_address: Optional[str] = Field(None, description="Customer IP address")
    device_fingerprint: Optional[str] = Field(None, description="Device identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "merchant_id": "merch_001",
                "amount": 4999.00,
                "payment_method": "CARD",
                "card_last4": "4242",
                "customer_email": "shopper@example.com",
                "ip_address": "106.51.75.142",
                "device_fingerprint": "fp_abc123xyz"
            }
        }


class CheckoutEvaluationResponse(BaseModel):
    """Real-time checkout risk evaluation response"""
    transaction_id: str = Field(..., description="Generated transaction ID")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    decision: RiskDecision = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    signals: List[EvidenceSignal] = Field(..., description="Evidence signals")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    allow_transaction: bool = Field(..., description="Whether to allow transaction")
    fraud_probability: Optional[float] = Field(default=None, description="Calibrated statistical fraud probability (0.0 to 1.0)")
    user_facing_title: Optional[str] = Field(default=None, description="Simplified user-facing status title")
    user_facing_message: Optional[str] = Field(default=None, description="Simplified user-facing message")
    optimal_threshold: Optional[float] = Field(default=None, description="Decision threshold calibrated on validation data")
    model_version: Optional[str] = Field(default=None, description="Trained model version")
    website_context: Optional[dict] = Field(default=None, description="Merchant website verification telemetry")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "txn_20260903_sim_001",
                "risk_score": 18.5,
                "risk_level": "LOW",
                "decision": "ALLOW",
                "confidence": 91.0,
                "signals": [],
                "processing_time_ms": 42.3,
                "allow_transaction": True
            }
        }


class SimulatorRequest(BaseModel):
    """Risk simulator calculation request"""
    amount: float = Field(..., gt=0, le=500000, description="Transaction amount")
    payment_method: PaymentMethod = Field(..., description="Payment method")
    velocity_1h: int = Field(..., ge=0, le=50, description="Transactions in last hour")
    failed_attempts_15m: int = Field(default=0, ge=0, le=10, description="Failed attempts in 15 minutes")
    merchant_risk_level: RiskLevel = Field(..., description="Merchant risk level")
    customer_account_age_days: int = Field(..., ge=0, le=3650, description="Customer account age")

    class Config:
        json_schema_extra = {
            "example": {
                "amount": 25000.00,
                "payment_method": "CARD",
                "velocity_1h": 1,
                "failed_attempts_15m": 0,
                "merchant_risk_level": "LOW",
                "customer_account_age_days": 365
            }
        }


class SimulatorResponse(BaseModel):
    """Risk simulator calculation response"""
    risk_score: float = Field(..., ge=0, le=100, description="Calculated risk score")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    decision: RiskDecision = Field(..., description="Recommended action")
    confidence: float = Field(..., ge=0, le=100, description="Confidence percentage")
    contributing_factors: List[str] = Field(..., description="Factors that influenced the score")
    calculation_breakdown: dict = Field(..., description="Detailed score breakdown")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_score": 32.5,
                "risk_level": "MEDIUM",
                "decision": "MONITOR",
                "confidence": 85.0,
                "contributing_factors": [
                    "High transaction amount (₹25,000)",
                    "Merchant risk level: LOW"
                ],
                "calculation_breakdown": {
                    "base_score": 20,
                    "amount_factor": 8.5,
                    "velocity_factor": 0,
                    "merchant_factor": 4
                }
            }
        }


# ============================================================================
# EVIDENCE & SIGNALS MODELS
# ============================================================================

class SignalCatalogResponse(BaseModel):
    """Complete signal catalog response"""
    signals: List[EvidenceSignal] = Field(..., description="All available signals")
    categories: List[str] = Field(..., description="Available categories")
    total_count: int = Field(..., description="Total signal count")

    class Config:
        json_schema_extra = {
            "example": {
                "signals": [],
                "categories": ["WEBSITE", "IDENTITY", "VELOCITY", "PAYMENT", "NETWORK"],
                "total_count": 24
            }
        }


# ============================================================================
# ANALYTICS MODELS
# ============================================================================

class DashboardOverview(BaseModel):
    """Dashboard overview metrics"""
    total_transactions: int = Field(..., description="Total transactions evaluated")
    total_volume_inr: float = Field(..., description="Total transaction volume in INR")
    flagged_transactions: int = Field(..., description="Flagged transaction count")
    flagged_percentage: float = Field(..., description="Percentage of flagged transactions")
    high_risk_merchants: int = Field(..., description="High-risk merchant count")
    manual_review_rate: float = Field(..., description="Manual review rate percentage")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Snapshot timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "total_transactions": 14290,
                "total_volume_inr": 48000000.00,
                "flagged_transactions": 86,
                "flagged_percentage": 0.60,
                "high_risk_merchants": 12,
                "manual_review_rate": 3.4,
                "timestamp": "2026-09-03T10:30:00Z"
            }
        }


class RiskDistribution(BaseModel):
    """Risk level distribution"""
    low: int = Field(..., description="Low-risk count")
    medium: int = Field(..., description="Medium-risk count")
    high: int = Field(..., description="High-risk count")

    class Config:
        json_schema_extra = {
            "example": {
                "low": 13800,
                "medium": 404,
                "high": 86
            }
        }


class TimeSeriesDataPoint(BaseModel):
    """Single time series data point"""
    timestamp: datetime = Field(..., description="Data point timestamp")
    value: float = Field(..., description="Metric value")

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2026-09-03T10:00:00Z",
                "value": 1250.0
            }
        }


class AnalyticsOverview(BaseModel):
    """Complete analytics overview"""
    risk_distribution: RiskDistribution = Field(..., description="Risk level distribution")
    transaction_volume_24h: List[TimeSeriesDataPoint] = Field(..., description="24-hour transaction volume")
    flagged_volume_24h: List[TimeSeriesDataPoint] = Field(..., description="24-hour flagged volume")
    decision_distribution: dict = Field(..., description="Decision type distribution")
    payment_method_breakdown: dict = Field(..., description="Payment method breakdown")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_distribution": {"low": 13800, "medium": 404, "high": 86},
                "transaction_volume_24h": [],
                "flagged_volume_24h": [],
                "decision_distribution": {
                    "ALLOW": 13500,
                    "MONITOR": 650,
                    "REQUIRE_REVIEW": 120,
                    "BLOCK_DEMO_PAYMENT": 20
                },
                "payment_method_breakdown": {
                    "CARD": 8574,
                    "UPI": 5234,
                    "NETBANKING": 482
                }
            }
        }


# ============================================================================
# MODEL STATUS MODELS
# ============================================================================

class ModelMetrics(BaseModel):
    """ML model performance metrics"""
    precision: Optional[float] = Field(None, ge=0, le=1, description="Precision score")
    recall: Optional[float] = Field(None, ge=0, le=1, description="Recall score")
    f1_score: Optional[float] = Field(None, ge=0, le=1, description="F1 score")
    roc_auc: Optional[float] = Field(None, ge=0, le=1, description="ROC-AUC score")
    accuracy: Optional[float] = Field(None, ge=0, le=1, description="Accuracy score")

    class Config:
        json_schema_extra = {
            "example": {
                "precision": 0.94,
                "recall": 0.89,
                "f1_score": 0.91,
                "roc_auc": 0.96,
                "accuracy": 0.92
            }
        }


class ModelStatus(BaseModel):
    """ML model status and specifications"""
    model_name: str = Field(..., description="Model identifier")
    model_type: str = Field(..., description="Model architecture type")
    status: str = Field(..., description="Current status")
    version: str = Field(..., description="Model version")
    target_latency_ms: float = Field(..., description="Target latency")
    current_latency_ms: Optional[float] = Field(None, description="Current latency")
    metrics: Optional[ModelMetrics] = Field(None, description="Performance metrics")
    last_trained: Optional[datetime] = Field(None, description="Last training timestamp")
    description: str = Field(..., description="Model description")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "merchant_risk_classifier",
                "model_type": "Random Forest",
                "status": "MOCK_READY",
                "version": "1.0.0-dev",
                "target_latency_ms": 85.0,
                "current_latency_ms": 42.3,
                "metrics": None,
                "last_trained": None,
                "description": "Merchant domain risk classification model"
            }
        }


class ModelsStatusResponse(BaseModel):
    """Complete model status response"""
    models: List[ModelStatus] = Field(..., description="All model statuses")
    demo_mode: bool = Field(default=True, description="Demo mode indicator")
    note: str = Field(..., description="Status note")

    class Config:
        json_schema_extra = {
            "example": {
                "models": [],
                "demo_mode": True,
                "note": "Awaiting live ground-truth settlement data for training"
            }
        }


# ============================================================================
# ERROR RESPONSE MODELS
# ============================================================================

class ErrorDetail(BaseModel):
    """Error detail structure"""
    field: Optional[str] = Field(None, description="Field that caused error")
    message: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Application error code")


class ErrorResponse(BaseModel):
    """Standardized error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[List[ErrorDetail]] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "VALIDATION_ERROR",
                "message": "Invalid request parameters",
                "details": [
                    {
                        "field": "amount",
                        "message": "Amount must be greater than 0",
                        "error_code": "VALUE_ERROR"
                    }
                ],
                "request_id": "req_abc123"
            }
        }


# ============================================================================
# HEALTH CHECK MODELS
# ============================================================================

class HealthCheckResponse(BaseModel):
    """Health check response with granular service status"""
    status: str = Field(default="ok", description="Overall service status")
    version: str = Field(default="1.0.0", description="API version")
    demo_mode: bool = Field(default=True, description="Demo mode indicator")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Current timestamp")
    services: Dict[str, str] = Field(
        default_factory=lambda: {
            "backend": "connected",
            "ml_model": "ready",
            "database": "connected",
            "website_analysis": "ready",
            "payment_gateway": "demo"
        },
        description="Detailed service connectivity and subsystem health"
    )

    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "status": "ok",
                "version": "1.0.0",
                "demo_mode": True,
                "timestamp": "2026-09-05T08:30:00Z",
                "services": {
                    "backend": "connected",
                    "ml_model": "ready",
                    "database": "connected",
                    "website_analysis": "ready",
                    "payment_gateway": "demo"
                }
            }
        }
