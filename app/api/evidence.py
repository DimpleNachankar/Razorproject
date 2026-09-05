"""
Evidence & Signal Library API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.schemas import SignalCatalogResponse, EvidenceSignal
from app.mock_data import get_signal_catalog, get_signal_by_id
from app.config import ErrorCodes

router = APIRouter(prefix="/evidence", tags=["Evidence"])


@router.get(
    "/signals",
    response_model=SignalCatalogResponse,
    summary="Get Signal Catalog",
    description="""
    Retrieve complete catalog of evidence signals tracked by TrustShield.
    
    The signal catalog includes:
    - WEBSITE signals (domain age, SSL, etc.)
    - IDENTITY signals (refund policy, contact info, etc.)
    - VELOCITY signals (transaction frequency, etc.)
    - PAYMENT signals (amount, method, failures, etc.)
    - NETWORK signals (IP location, device fingerprint, etc.)
    
    Each signal includes:
    - Impact level (LOW/MEDIUM/HIGH)
    - Confidence score
    - Provenance (data source)
    - Description and interpretation
    """
)
async def get_signals(
    category: Optional[str] = Query(None, description="Filter by category (WEBSITE, IDENTITY, VELOCITY, PAYMENT, NETWORK)")
):
    """
    Get all evidence signals with optional category filter
    """
    
    signals = get_signal_catalog()
    
    # Apply category filter if provided
    if category:
        category_upper = category.upper()
        signals = [s for s in signals if s.category.value == category_upper]
    
    # Get unique categories
    categories = list(set(signal.category.value for signal in get_signal_catalog()))
    
    return SignalCatalogResponse(
        signals=signals,
        categories=categories,
        total_count=len(signals)
    )


@router.get(
    "/signals/{signal_id}",
    response_model=EvidenceSignal,
    summary="Get Signal Details",
    description="""
    Retrieve detailed information about a specific evidence signal.
    
    Useful for understanding:
    - How the signal is calculated
    - What data sources are used
    - Impact on risk scoring
    - False positive mitigation
    """
)
async def get_signal(signal_id: str):
    """
    Get specific signal by ID
    """
    
    signal = get_signal_by_id(signal_id)
    
    if not signal:
        raise HTTPException(
            status_code=404,
            detail={
                "error": ErrorCodes.SIGNAL_NOT_FOUND,
                "message": f"Signal with ID '{signal_id}' not found"
            }
        )
    
    return signal


@router.get(
    "/categories",
    summary="Get Signal Categories",
    description="""
    Get list of all signal categories.
    
    Returns category metadata including:
    - Category name
    - Description
    - Number of signals
    """
)
async def get_categories():
    """
    Get all signal categories with metadata
    """
    
    signals = get_signal_catalog()
    
    # Group signals by category
    category_groups = {}
    for signal in signals:
        category = signal.category.value
        if category not in category_groups:
            category_groups[category] = []
        category_groups[category].append(signal)
    
    # Build category metadata
    categories = []
    
    category_descriptions = {
        "WEBSITE": "Domain and website infrastructure signals",
        "IDENTITY": "Business identity and verification signals",
        "VELOCITY": "Transaction frequency and pattern signals",
        "PAYMENT": "Payment method and transaction signals",
        "NETWORK": "Network and device signals"
    }
    
    for category_name, category_signals in category_groups.items():
        categories.append({
            "name": category_name,
            "description": category_descriptions.get(category_name, "Signal category"),
            "signal_count": len(category_signals),
            "example_signals": [s.title for s in category_signals[:3]]
        })
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }


@router.get(
    "/impact-analysis",
    summary="Get Signal Impact Analysis",
    description="""
    Analyze the impact distribution of signals.
    
    Shows how signals contribute to risk scoring:
    - High impact signals
    - Medium impact signals
    - Low impact signals
    """
)
async def get_impact_analysis():
    """
    Get signal impact distribution
    """
    
    signals = get_signal_catalog()
    
    # Count by impact level
    impact_distribution = {
        "HIGH": len([s for s in signals if s.impact.value == "HIGH"]),
        "MEDIUM": len([s for s in signals if s.impact.value == "MEDIUM"]),
        "LOW": len([s for s in signals if s.impact.value == "LOW"])
    }
    
    # Get high impact signals
    high_impact_signals = [
        {
            "title": s.title,
            "category": s.category.value,
            "description": s.description
        }
        for s in signals if s.impact.value == "HIGH"
    ]
    
    return {
        "impact_distribution": impact_distribution,
        "high_impact_signals": high_impact_signals,
        "total_signals": len(signals),
        "note": "High impact signals contribute most significantly to risk scores"
    }


@router.get(
    "/provenance",
    summary="Get Signal Provenance Information",
    description="""
    Get information about signal data sources.
    
    Shows where signals come from:
    - DNS scans
    - Content evaluation
    - Payment gateway
    - Consortium data
    - Velocity tracking
    - Device fingerprinting
    """
)
async def get_provenance_info():
    """
    Get signal provenance breakdown
    """
    
    signals = get_signal_catalog()
    
    # Group by provenance
    provenance_groups = {}
    for signal in signals:
        prov = signal.provenance.value
        if prov not in provenance_groups:
            provenance_groups[prov] = []
        provenance_groups[prov].append(signal.title)
    
    provenance_descriptions = {
        "DNS_SCAN": "Domain registration and DNS infrastructure analysis",
        "CONTENT_EVAL": "Website content and policy detection",
        "PAYMENT_GATEWAY": "Payment processing and transaction data",
        "CONSORTIUM_MOCK": "Simulated consortium and business registry data",
        "VELOCITY_TRACKER": "Real-time transaction frequency monitoring",
        "DEVICE_FINGERPRINT": "Device and network analysis"
    }
    
    provenances = []
    for prov_name, prov_signals in provenance_groups.items():
        provenances.append({
            "name": prov_name,
            "description": provenance_descriptions.get(prov_name, "Data source"),
            "signal_count": len(prov_signals),
            "signals": prov_signals
        })
    
    return {
        "provenances": provenances,
        "total_sources": len(provenances)
    }
