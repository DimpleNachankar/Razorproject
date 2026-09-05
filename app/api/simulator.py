"""
Risk Simulator API Endpoints
Interactive risk calculation playground
"""

from fastapi import APIRouter
from app.schemas import SimulatorRequest, SimulatorResponse
from app.risk_engine import calculate_simulator_risk

router = APIRouter(prefix="/simulator", tags=["Simulator"])


@router.post(
    "/calculate",
    response_model=SimulatorResponse,
    summary="Calculate Risk Score",
    description="""
    Interactive risk score calculation for testing scenarios.
    
    Allows dynamic adjustment of:
    - Transaction amount
    - Payment method
    - Transaction velocity
    - Failed payment attempts
    - Merchant risk level
    - Customer account age
    
    Returns:
    - Calculated risk score (0-100)
    - Risk level (LOW/MEDIUM/HIGH)
    - Recommended decision
    - Contributing factors
    - Detailed calculation breakdown
    
    **Use Cases**:
    - Understanding risk factors
    - Testing threshold configurations
    - Demo scenarios
    - Policy calibration
    """
)
async def calculate_risk(request: SimulatorRequest):
    """
    Calculate risk score based on provided parameters
    """
    
    result = calculate_simulator_risk(
        amount=request.amount,
        payment_method=request.payment_method,
        velocity_1h=request.velocity_1h,
        failed_attempts_15m=request.failed_attempts_15m,
        merchant_risk_level=request.merchant_risk_level,
        customer_account_age_days=request.customer_account_age_days
    )
    
    return SimulatorResponse(
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        decision=result["decision"],
        confidence=result["confidence"],
        contributing_factors=result["contributing_factors"],
        calculation_breakdown=result["calculation_breakdown"]
    )


@router.get(
    "/presets",
    summary="Get Simulator Presets",
    description="""
    Get predefined simulator scenarios for quick testing.
    
    Includes common patterns:
    - Normal purchase
    - High-velocity attack
    - High-value first-time buyer
    - Card testing pattern
    - Suspicious merchant checkout
    """
)
async def get_simulator_presets():
    """
    Return predefined simulator scenarios
    """
    
    return {
        "presets": [
            {
                "id": "normal_purchase",
                "name": "Normal Purchase",
                "description": "Typical low-risk transaction",
                "parameters": {
                    "amount": 2499.0,
                    "payment_method": "CARD",
                    "velocity_1h": 1,
                    "failed_attempts_15m": 0,
                    "merchant_risk_level": "LOW",
                    "customer_account_age_days": 365
                },
                "expected_outcome": {
                    "risk_level": "LOW",
                    "decision": "ALLOW"
                }
            },
            {
                "id": "high_velocity_attack",
                "name": "High-Velocity Attack",
                "description": "Suspicious rapid transaction pattern",
                "parameters": {
                    "amount": 15000.0,
                    "payment_method": "CARD",
                    "velocity_1h": 12,
                    "failed_attempts_15m": 3,
                    "merchant_risk_level": "MEDIUM",
                    "customer_account_age_days": 180
                },
                "expected_outcome": {
                    "risk_level": "HIGH",
                    "decision": "BLOCK_DEMO_PAYMENT"
                }
            },
            {
                "id": "high_value_first_time",
                "name": "High-Value First-Time Buyer",
                "description": "Large purchase from new customer",
                "parameters": {
                    "amount": 89000.0,
                    "payment_method": "CARD",
                    "velocity_1h": 1,
                    "failed_attempts_15m": 0,
                    "merchant_risk_level": "LOW",
                    "customer_account_age_days": 2
                },
                "expected_outcome": {
                    "risk_level": "HIGH",
                    "decision": "REQUIRE_REVIEW"
                }
            },
            {
                "id": "card_testing",
                "name": "Card Testing Pattern",
                "description": "Multiple small failed attempts",
                "parameters": {
                    "amount": 100.0,
                    "payment_method": "CARD",
                    "velocity_1h": 8,
                    "failed_attempts_15m": 5,
                    "merchant_risk_level": "MEDIUM",
                    "customer_account_age_days": 1
                },
                "expected_outcome": {
                    "risk_level": "HIGH",
                    "decision": "BLOCK_DEMO_PAYMENT"
                }
            },
            {
                "id": "suspicious_merchant",
                "name": "Suspicious Merchant Checkout",
                "description": "High-risk merchant transaction",
                "parameters": {
                    "amount": 25000.0,
                    "payment_method": "CARD",
                    "velocity_1h": 2,
                    "failed_attempts_15m": 0,
                    "merchant_risk_level": "HIGH",
                    "customer_account_age_days": 90
                },
                "expected_outcome": {
                    "risk_level": "HIGH",
                    "decision": "REQUIRE_REVIEW"
                }
            },
            {
                "id": "safe_upi",
                "name": "Safe UPI Transaction",
                "description": "Low-risk UPI payment",
                "parameters": {
                    "amount": 5000.0,
                    "payment_method": "UPI",
                    "velocity_1h": 1,
                    "failed_attempts_15m": 0,
                    "merchant_risk_level": "LOW",
                    "customer_account_age_days": 540
                },
                "expected_outcome": {
                    "risk_level": "LOW",
                    "decision": "ALLOW"
                }
            }
        ]
    }


@router.post(
    "/batch-calculate",
    summary="Batch Risk Calculation",
    description="""
    Calculate risk scores for multiple scenarios at once.
    
    Useful for:
    - Comparing different scenarios
    - Testing threshold changes
    - Policy impact analysis
    """
)
async def batch_calculate(scenarios: list[SimulatorRequest]):
    """
    Calculate risk for multiple scenarios
    """
    
    results = []
    
    for idx, scenario in enumerate(scenarios):
        result = calculate_simulator_risk(
            amount=scenario.amount,
            payment_method=scenario.payment_method,
            velocity_1h=scenario.velocity_1h,
            failed_attempts_15m=scenario.failed_attempts_15m,
            merchant_risk_level=scenario.merchant_risk_level,
            customer_account_age_days=scenario.customer_account_age_days
        )
        
        results.append({
            "scenario_index": idx,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"].value,
            "decision": result["decision"].value,
            "confidence": result["confidence"]
        })
    
    return {
        "total_scenarios": len(scenarios),
        "results": results,
        "summary": {
            "allow": len([r for r in results if r["decision"] == "ALLOW"]),
            "monitor": len([r for r in results if r["decision"] == "MONITOR"]),
            "require_review": len([r for r in results if r["decision"] == "REQUIRE_REVIEW"]),
            "block": len([r for r in results if r["decision"] == "BLOCK_DEMO_PAYMENT"])
        }
    }
