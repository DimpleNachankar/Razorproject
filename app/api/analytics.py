"""
Analytics & Operational Insights API Endpoints
"""

from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Optional

from app.schemas import AnalyticsOverview, RiskDistribution, TimeSeriesDataPoint
from app.mock_data import (
    get_all_transactions,
    get_risk_distribution,
    get_decision_distribution,
    get_payment_method_breakdown
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
    summary="Get Analytics Overview",
    description="""
    Comprehensive analytics overview.
    
    Includes:
    - Risk level distribution
    - Transaction volume trends (24h)
    - Flagged transaction trends
    - Decision distribution
    - Payment method breakdown
    """
)
async def get_analytics_overview(
    timeframe: str = Query("24h", description="Timeframe (24h, 7d, 30d)")
):
    """
    Get complete analytics overview
    """
    
    # Get risk distribution
    risk_dist_data = get_risk_distribution()
    risk_distribution = RiskDistribution(
        low=risk_dist_data["low"],
        medium=risk_dist_data["medium"],
        high=risk_dist_data["high"]
    )
    
    # Generate mock time series data for 24 hours
    transaction_volume_24h = []
    flagged_volume_24h = []
    
    now = datetime.utcnow()
    for hour in range(24):
        timestamp = now - timedelta(hours=23-hour)
        
        # Mock volume data (higher during business hours)
        hour_of_day = timestamp.hour
        if 9 <= hour_of_day <= 21:  # Business hours
            volume = 450 + (hour * 15)
            flagged = 3 + (hour % 5)
        else:  # Off hours
            volume = 150 + (hour * 5)
            flagged = 1 + (hour % 3)
        
        transaction_volume_24h.append(TimeSeriesDataPoint(
            timestamp=timestamp,
            value=float(volume)
        ))
        
        flagged_volume_24h.append(TimeSeriesDataPoint(
            timestamp=timestamp,
            value=float(flagged)
        ))
    
    # Get decision and payment method distributions
    decision_dist = get_decision_distribution()
    payment_method_dist = get_payment_method_breakdown()
    
    return AnalyticsOverview(
        risk_distribution=risk_distribution,
        transaction_volume_24h=transaction_volume_24h,
        flagged_volume_24h=flagged_volume_24h,
        decision_distribution=decision_dist,
        payment_method_breakdown=payment_method_dist
    )


@router.get(
    "/trends",
    summary="Get Risk Trends",
    description="""
    Get risk score trends over time.
    
    Useful for:
    - Detecting drift in risk patterns
    - Monitoring system performance
    - Identifying seasonal patterns
    """
)
async def get_risk_trends(
    timeframe: str = Query("7d", description="Timeframe (24h, 7d, 30d)"),
    granularity: str = Query("hour", description="Data granularity (hour, day)")
):
    """
    Get risk trends over specified timeframe
    """
    
    transactions = get_all_transactions()
    
    # Calculate average risk scores over time
    now = datetime.utcnow()
    
    if timeframe == "24h":
        periods = 24
        period_hours = 1
    elif timeframe == "7d":
        periods = 7
        period_hours = 24
    else:  # 30d
        periods = 30
        period_hours = 24
    
    trends = []
    for i in range(periods):
        period_start = now - timedelta(hours=(periods - i) * period_hours)
        
        # Filter transactions in this period
        period_txns = [
            t for t in transactions
            if period_start <= t.timestamp < period_start + timedelta(hours=period_hours)
        ]
        
        if period_txns:
            avg_risk = sum(t.risk_score for t in period_txns) / len(period_txns)
            txn_count = len(period_txns)
        else:
            avg_risk = 0
            txn_count = 0
        
        trends.append({
            "timestamp": period_start.isoformat(),
            "average_risk_score": round(avg_risk, 2),
            "transaction_count": txn_count
        })
    
    return {
        "timeframe": timeframe,
        "granularity": granularity,
        "trends": trends,
        "summary": {
            "current_avg_risk": round(trends[-1]["average_risk_score"], 2) if trends else 0,
            "total_transactions": sum(t["transaction_count"] for t in trends)
        }
    }


@router.get(
    "/merchant-risk-distribution",
    summary="Get Merchant Risk Distribution",
    description="""
    Analyze risk distribution across merchants.
    
    Shows:
    - Percentage of merchants in each risk category
    - High-risk merchant details
    - Category-based risk patterns
    """
)
async def get_merchant_risk_distribution():
    """
    Get merchant risk distribution
    """
    
    from app.mock_data import get_all_merchants
    
    merchants = get_all_merchants()
    
    # Risk level distribution
    risk_distribution = {
        "LOW": len([m for m in merchants if m.risk_level.value == "LOW"]),
        "MEDIUM": len([m for m in merchants if m.risk_level.value == "MEDIUM"]),
        "HIGH": len([m for m in merchants if m.risk_level.value == "HIGH"])
    }
    
    # Category risk analysis
    category_risk = {}
    for merchant in merchants:
        category = merchant.category
        if category not in category_risk:
            category_risk[category] = {
                "total": 0,
                "avg_risk_score": 0,
                "high_risk_count": 0
            }
        
        category_risk[category]["total"] += 1
        category_risk[category]["avg_risk_score"] += merchant.risk_score
        if merchant.risk_level.value == "HIGH":
            category_risk[category]["high_risk_count"] += 1
    
    # Calculate averages
    for category in category_risk:
        total = category_risk[category]["total"]
        category_risk[category]["avg_risk_score"] = round(
            category_risk[category]["avg_risk_score"] / total, 2
        )
    
    # Get high-risk merchants
    high_risk_merchants = [
        {
            "id": m.id,
            "name": m.name,
            "domain": m.domain,
            "risk_score": m.risk_score,
            "decision": m.decision.value
        }
        for m in merchants if m.risk_level.value == "HIGH"
    ]
    
    return {
        "risk_distribution": risk_distribution,
        "total_merchants": len(merchants),
        "category_analysis": category_risk,
        "high_risk_merchants": high_risk_merchants
    }


@router.get(
    "/payment-method-analysis",
    summary="Get Payment Method Analysis",
    description="""
    Analyze risk patterns by payment method.
    
    Compares:
    - Average risk scores by method
    - Transaction volumes
    - Fraud rates
    """
)
async def get_payment_method_analysis():
    """
    Analyze risk by payment method
    """
    
    transactions = get_all_transactions()
    
    # Group by payment method
    method_analysis = {}
    
    for txn in transactions:
        method = txn.method.value
        
        if method not in method_analysis:
            method_analysis[method] = {
                "count": 0,
                "total_amount": 0,
                "total_risk_score": 0,
                "high_risk_count": 0,
                "blocked_count": 0
            }
        
        method_analysis[method]["count"] += 1
        method_analysis[method]["total_amount"] += txn.amount
        method_analysis[method]["total_risk_score"] += txn.risk_score
        
        if txn.risk_level.value == "HIGH":
            method_analysis[method]["high_risk_count"] += 1
        
        if txn.decision.value == "BLOCK_DEMO_PAYMENT":
            method_analysis[method]["blocked_count"] += 1
    
    # Calculate averages and rates
    for method in method_analysis:
        count = method_analysis[method]["count"]
        method_analysis[method]["avg_amount"] = round(
            method_analysis[method]["total_amount"] / count, 2
        )
        method_analysis[method]["avg_risk_score"] = round(
            method_analysis[method]["total_risk_score"] / count, 2
        )
        method_analysis[method]["high_risk_rate"] = round(
            (method_analysis[method]["high_risk_count"] / count) * 100, 2
        )
        method_analysis[method]["block_rate"] = round(
            (method_analysis[method]["blocked_count"] / count) * 100, 2
        )
    
    return {
        "payment_methods": method_analysis,
        "total_transactions": len(transactions),
        "note": "Analysis based on historical transaction data"
    }


@router.get(
    "/velocity-patterns",
    summary="Get Velocity Pattern Analysis",
    description="""
    Analyze transaction velocity patterns.
    
    Identifies:
    - High-velocity transactions
    - Velocity-based risk correlation
    - Suspicious patterns
    """
)
async def get_velocity_patterns():
    """
    Analyze transaction velocity patterns
    """
    
    transactions = get_all_transactions()
    
    # Group by velocity
    velocity_groups = {
        "normal": [],  # 1-3 txns/hour
        "elevated": [],  # 4-6 txns/hour
        "high": [],  # 7-10 txns/hour
        "suspicious": []  # >10 txns/hour
    }
    
    for txn in transactions:
        velocity = txn.velocity_1h
        
        if velocity <= 3:
            velocity_groups["normal"].append(txn)
        elif velocity <= 6:
            velocity_groups["elevated"].append(txn)
        elif velocity <= 10:
            velocity_groups["high"].append(txn)
        else:
            velocity_groups["suspicious"].append(txn)
    
    # Calculate statistics for each group
    analysis = {}
    for group_name, group_txns in velocity_groups.items():
        if group_txns:
            avg_risk = sum(t.risk_score for t in group_txns) / len(group_txns)
            high_risk_count = len([t for t in group_txns if t.risk_level.value == "HIGH"])
        else:
            avg_risk = 0
            high_risk_count = 0
        
        analysis[group_name] = {
            "transaction_count": len(group_txns),
            "avg_risk_score": round(avg_risk, 2),
            "high_risk_count": high_risk_count,
            "percentage": round((len(group_txns) / len(transactions)) * 100, 2)
        }
    
    return {
        "velocity_analysis": analysis,
        "total_transactions": len(transactions),
        "note": "Velocity patterns indicate potential fraud activity"
    }
