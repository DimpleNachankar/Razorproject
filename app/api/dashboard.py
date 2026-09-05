"""
Dashboard Overview API Endpoints
"""

from fastapi import APIRouter
from datetime import datetime

from app.schemas import DashboardOverview
from app.mock_data import get_dashboard_stats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/overview",
    response_model=DashboardOverview,
    summary="Get Dashboard Overview",
    description="""
    Get high-level dashboard metrics and system overview.
    
    Includes:
    - Total transactions evaluated
    - Total transaction volume (INR)
    - Flagged transaction count and percentage
    - High-risk merchant count
    - Manual review rate
    
    This provides a snapshot of system activity and performance.
    """
)
async def get_dashboard_overview():
    """
    Get dashboard overview metrics
    """
    
    stats = get_dashboard_stats()
    
    return DashboardOverview(
        total_transactions=stats["total_transactions"],
        total_volume_inr=stats["total_volume_inr"],
        flagged_transactions=stats["flagged_transactions"],
        flagged_percentage=stats["flagged_percentage"],
        high_risk_merchants=stats["high_risk_merchants"],
        manual_review_rate=stats["manual_review_rate"],
        timestamp=datetime.utcnow()
    )


@router.get(
    "/system-health",
    summary="Get System Health",
    description="""
    Get system health metrics and status.
    
    Includes:
    - Engine status
    - Processing latency
    - Error rates
    - System uptime
    """
)
async def get_system_health():
    """
    Get system health metrics
    """
    
    return {
        "status": "healthy",
        "engine_status": "active",
        "demo_mode": True,
        "processing_metrics": {
            "avg_merchant_analysis_ms": 42.3,
            "avg_transaction_eval_ms": 28.5,
            "p95_latency_ms": 78.4,
            "p99_latency_ms": 94.2
        },
        "error_rates": {
            "analysis_errors": 0.0,
            "evaluation_errors": 0.0,
            "api_errors": 0.0
        },
        "uptime": {
            "uptime_percentage": 99.9,
            "last_restart": None
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get(
    "/activity-feed",
    summary="Get Recent Activity Feed",
    description="""
    Get recent risk-related activity for monitoring.
    
    Shows:
    - Recent high-risk transactions
    - New merchant analyses
    - Blocked transactions
    - Manual review requests
    """
)
async def get_activity_feed(limit: int = 20):
    """
    Get recent activity feed
    """
    
    from app.mock_data import get_recent_transactions, get_all_merchants
    
    recent_txns = get_recent_transactions(limit=limit)
    
    # Build activity feed
    activities = []
    
    for txn in recent_txns:
        activity_type = "transaction_evaluated"
        severity = "info"
        
        if txn.decision.value == "BLOCK_DEMO_PAYMENT":
            activity_type = "transaction_blocked"
            severity = "critical"
        elif txn.decision.value == "REQUIRE_REVIEW":
            activity_type = "review_required"
            severity = "warning"
        elif txn.risk_level.value == "HIGH":
            activity_type = "high_risk_detected"
            severity = "warning"
        
        activities.append({
            "id": txn.id,
            "type": activity_type,
            "severity": severity,
            "title": f"{activity_type.replace('_', ' ').title()}",
            "description": f"{txn.merchant_name} - ₹{txn.amount:,.2f} ({txn.method.value})",
            "risk_score": txn.risk_score,
            "decision": txn.decision.value,
            "timestamp": txn.timestamp.isoformat()
        })
    
    return {
        "activities": activities,
        "total": len(activities),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get(
    "/alerts",
    summary="Get Active Alerts",
    description="""
    Get active system alerts and warnings.
    
    Types of alerts:
    - High-risk transaction surge
    - New suspicious merchant
    - Velocity threshold breach
    - System performance issues
    """
)
async def get_alerts():
    """
    Get active system alerts
    """
    
    from app.mock_data import get_all_transactions, get_all_merchants
    
    transactions = get_all_transactions()
    merchants = get_all_merchants()
    
    alerts = []
    
    # Check for high-risk transaction surge
    high_risk_txns = [t for t in transactions if t.risk_level.value == "HIGH"]
    high_risk_percentage = (len(high_risk_txns) / len(transactions)) * 100
    
    if high_risk_percentage > 5:
        alerts.append({
            "id": "alert_001",
            "type": "high_risk_surge",
            "severity": "warning",
            "title": "Elevated High-Risk Transaction Rate",
            "description": f"{len(high_risk_txns)} high-risk transactions ({high_risk_percentage:.1f}%) detected",
            "recommendation": "Review recent transactions and adjust thresholds if needed",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    # Check for suspicious merchants
    suspicious_merchants = [m for m in merchants if m.risk_score > 80]
    
    if suspicious_merchants:
        alerts.append({
            "id": "alert_002",
            "type": "suspicious_merchant",
            "severity": "critical",
            "title": f"{len(suspicious_merchants)} Suspicious Merchant(s) Detected",
            "description": "Merchants with risk scores above 80 require immediate review",
            "recommendation": "Review merchant profiles and consider blocking demo payments",
            "affected_merchants": [m.domain for m in suspicious_merchants[:5]],
            "timestamp": datetime.utcnow().isoformat()
        })
    
    # Check for velocity patterns
    high_velocity_txns = [t for t in transactions if t.velocity_1h > 8]
    
    if len(high_velocity_txns) > 10:
        alerts.append({
            "id": "alert_003",
            "type": "velocity_pattern",
            "severity": "warning",
            "title": "High-Velocity Pattern Detected",
            "description": f"{len(high_velocity_txns)} transactions with suspicious velocity (>8 txns/hour)",
            "recommendation": "Review velocity tracking rules and customer patterns",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    return {
        "alerts": alerts,
        "total_active": len(alerts),
        "last_checked": datetime.utcnow().isoformat(),
        "note": "Demo mode: Alerts are generated from mock data patterns"
    }


@router.get(
    "/quick-stats",
    summary="Get Quick Statistics",
    description="""
    Get quick statistics for dashboard widgets.
    
    Provides compact metrics for real-time monitoring.
    """
)
async def get_quick_stats():
    """
    Get quick statistics
    """
    
    from app.mock_data import (
        get_all_transactions,
        get_all_merchants,
        get_risk_distribution
    )
    
    transactions = get_all_transactions()
    merchants = get_all_merchants()
    risk_dist = get_risk_distribution()
    
    # Calculate quick stats
    total_volume = sum(t.amount for t in transactions)
    avg_amount = total_volume / len(transactions) if transactions else 0
    
    blocked_count = len([t for t in transactions if t.decision.value == "BLOCK_DEMO_PAYMENT"])
    review_count = len([t for t in transactions if t.decision.value == "REQUIRE_REVIEW"])
    
    return {
        "transactions": {
            "total": len(transactions),
            "total_volume_inr": round(total_volume, 2),
            "average_amount": round(avg_amount, 2),
            "blocked": blocked_count,
            "review_required": review_count
        },
        "merchants": {
            "total": len(merchants),
            "low_risk": len([m for m in merchants if m.risk_level.value == "LOW"]),
            "medium_risk": len([m for m in merchants if m.risk_level.value == "MEDIUM"]),
            "high_risk": len([m for m in merchants if m.risk_level.value == "HIGH"])
        },
        "risk_distribution": {
            "low": risk_dist["low"],
            "medium": risk_dist["medium"],
            "high": risk_dist["high"]
        },
        "timestamp": datetime.utcnow().isoformat()
    }
