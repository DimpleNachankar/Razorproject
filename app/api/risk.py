"""
Transaction Risk API Endpoints
Provides direct risk evaluation for transaction payment requests
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from app.risk_engine import evaluate_payment_with_ml
from app.mock_data import get_merchant_by_id

router = APIRouter(prefix="/risk", tags=["Risk"])


class TransactionPayload(BaseModel):
    amount: float = Field(..., description="Payment amount")
    payment_method: Optional[str] = Field(default="card", description="Payment method: card, upi, netbanking, wallet")
    currency: Optional[str] = Field(default="INR", description="Currency code")


class MerchantPayload(BaseModel):
    merchant_id: Optional[str] = Field(default="demo-001", description="Merchant ID")
    name: Optional[str] = Field(default=None, description="Merchant name")


class RiskEvaluationRequest(BaseModel):
    """
    Accepts nested { transaction: {...}, merchant: {...}, website: "..." }
    or top-level flat fields for maximum developer compatibility.
    """
    transaction: Optional[TransactionPayload] = None
    merchant: Optional[MerchantPayload] = None
    website: Optional[str] = None
    
    # Flat field fallbacks
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    merchant_id: Optional[str] = None


@router.post("/transaction")
async def evaluate_transaction_risk_endpoint(payload: RiskEvaluationRequest):
    """
    Evaluates transaction risk using the genuine trained ML model + website analyzer
    Returns calibrated fraud probability, decision (allow/review/block), and model details.
    """
    # Parse inputs cleanly from either nested or flat schema
    amount = 2499.0
    if payload.transaction and payload.transaction.amount is not None:
        amount = float(payload.transaction.amount)
    elif payload.amount is not None:
        amount = float(payload.amount)

    payment_method = "card"
    if payload.transaction and payload.transaction.payment_method:
        payment_method = payload.transaction.payment_method
    elif payload.payment_method:
        payment_method = payload.payment_method

    merchant_id = "demo-001"
    if payload.merchant and payload.merchant.merchant_id:
        merchant_id = payload.merchant.merchant_id
    elif payload.merchant_id:
        merchant_id = payload.merchant_id

    # Resolve merchant domain if available
    merchant_obj = get_merchant_by_id(merchant_id)
    website_url = payload.website or (merchant_obj.domain if merchant_obj else "democart.com")
    merchant_category = merchant_obj.category.value if (merchant_obj and hasattr(merchant_obj.category, 'value')) else "E_COMMERCE"

    # Evaluate with trained ML model + SSRF-safe website analyzer
    ml_eval = evaluate_payment_with_ml(
        amount=amount,
        payment_method=payment_method,
        merchant_category=merchant_category,
        merchant_url_or_domain=website_url,
        customer_context={
            'velocity_1h': 1,
            'account_age_days': 120,
            'failed_attempts': 0,
            'is_new_device': 0
        }
    )

    decision_str = "allow"
    if ml_eval['decision'].value == "ALLOW" or ml_eval['decision'] == "ALLOW":
        decision_str = "allow"
    elif ml_eval['decision'].value == "BLOCK_DEMO_PAYMENT" or ml_eval['decision'] == "BLOCK_DEMO_PAYMENT":
        decision_str = "block"
    else:
        decision_str = "review"

    return {
        "fraud_probability": ml_eval["fraud_probability"],
        "decision": decision_str,
        "risk_score": ml_eval["risk_score"],
        "risk_level": ml_eval["risk_level"].value if hasattr(ml_eval["risk_level"], "value") else str(ml_eval["risk_level"]),
        "model_version": ml_eval["model_version"],
        "optimal_threshold": ml_eval["optimal_threshold"],
        "confidence": ml_eval["confidence"],
        "user_facing_title": ml_eval["user_facing_title"],
        "user_facing_message": ml_eval["user_facing_message"],
        "website_context": ml_eval["website_context"],
        "signals": [
            {
                "id": s.id,
                "title": s.title,
                "value": s.value,
                "impact": s.impact.value if hasattr(s.impact, "value") else str(s.impact),
                "category": s.category.value if hasattr(s.category, "value") else str(s.category)
            }
            for s in ml_eval.get("signals", [])
        ],
        "timestamp": datetime.utcnow().isoformat()
    }
