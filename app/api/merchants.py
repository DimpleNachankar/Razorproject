"""
Merchant Risk Analysis API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
import time

from app.schemas import (
    MerchantRecord,
    MerchantAnalysisRequest,
    MerchantListResponse,
    ErrorResponse
)
from app.mock_data import (
    get_all_merchants,
    get_merchant_by_id,
    get_merchant_by_domain
)
from app.risk_engine import analyze_merchant_risk, estimate_domain_age
from app.config import ResponseMessages, ErrorCodes

router = APIRouter(prefix="/merchants", tags=["Merchants"])


@router.post(
    "/analyze",
    response_model=MerchantRecord,
    summary="Analyze Merchant Domain",
    description="""
    Analyze a merchant domain for risk assessment.
    
    Evaluates:
    - Domain age and registration
    - SSL/TLS certificate validity
    - Refund policy detection
    - Contact information completeness
    - Entity verification
    
    Returns complete merchant risk assessment with evidence signals.
    """
)
async def analyze_merchant(request: MerchantAnalysisRequest):
    """
    Analyze merchant domain and return risk assessment
    """
    
    domain = request.domain
    
    # Check if merchant already exists in mock data
    existing_merchant = get_merchant_by_domain(domain)
    if existing_merchant:
        return existing_merchant
    
    # Simulate analysis for new domain
    try:
        # Estimate domain characteristics (mock simulation)
        age_days = estimate_domain_age(domain)
        
        # Determine characteristics based on domain
        has_ssl = not any(domain.endswith(tld) for tld in [".xyz", ".top", ".work"])
        has_refund_policy = age_days > 180
        
        if age_days < 30:
            contact_quality = "Missing"
        elif age_days < 180:
            contact_quality = "Partial"
        else:
            contact_quality = "Complete"
        
        # Run risk analysis
        risk_score, risk_level, decision, confidence, signals = analyze_merchant_risk(
            domain=domain,
            age_days=age_days,
            has_ssl=has_ssl,
            has_refund_policy=has_refund_policy,
            contact_quality=contact_quality
        )
        
        # Build merchant record
        merchant = MerchantRecord(
            id=f"merch_dynamic_{int(time.time())}",
            name=domain.split(".")[0].title().replace("-", " "),
            domain=domain,
            category="General Commerce",
            age_days=age_days,
            risk_score=risk_score,
            risk_level=risk_level,
            decision=decision,
            confidence=confidence,
            signals=signals,
            refund_policy_detected=has_refund_policy,
            contact_score=contact_quality,
            created_at=datetime.utcnow(),
            last_evaluated=datetime.utcnow()
        )
        
        return merchant
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": ErrorCodes.INTERNAL_ERROR,
                "message": f"Failed to analyze merchant: {str(e)}"
            }
        )


@router.get(
    "",
    response_model=MerchantListResponse,
    summary="List Merchants",
    description="""
    List all merchants with optional filtering.
    
    Supports filtering by:
    - Risk level (low, medium, high)
    - Business category
    - Pagination
    """
)
async def list_merchants(
    risk_level: Optional[str] = Query(None, description="Filter by risk level (LOW, MEDIUM, HIGH)"),
    category: Optional[str] = Query(None, description="Filter by business category"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page")
):
    """
    Get paginated list of merchants with optional filters
    """
    
    merchants = get_all_merchants()
    
    # Apply filters
    if risk_level:
        risk_level_upper = risk_level.upper()
        merchants = [m for m in merchants if m.risk_level.value == risk_level_upper]
    
    if category:
        merchants = [m for m in merchants if category.lower() in m.category.lower()]
    
    total = len(merchants)
    
    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_merchants = merchants[start_idx:end_idx]
    
    return MerchantListResponse(
        merchants=paginated_merchants,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{merchant_id}",
    response_model=MerchantRecord,
    summary="Get Merchant Details",
    description="Retrieve detailed information about a specific merchant by ID."
)
async def get_merchant(merchant_id: str):
    """
    Get merchant by ID
    """
    
    merchant = get_merchant_by_id(merchant_id)
    
    if not merchant:
        raise HTTPException(
            status_code=404,
            detail={
                "error": ErrorCodes.MERCHANT_NOT_FOUND,
                "message": f"Merchant with ID '{merchant_id}' not found"
            }
        )
    
    return merchant


@router.get(
    "/domain/{domain}",
    response_model=MerchantRecord,
    summary="Get Merchant by Domain",
    description="Retrieve merchant information by domain name."
)
async def get_merchant_by_domain_endpoint(domain: str):
    """
    Get merchant by domain name
    """
    
    merchant = get_merchant_by_domain(domain)
    
    if not merchant:
        raise HTTPException(
            status_code=404,
            detail={
                "error": ErrorCodes.MERCHANT_NOT_FOUND,
                "message": f"Merchant with domain '{domain}' not found"
            }
        )
    
    return merchant
