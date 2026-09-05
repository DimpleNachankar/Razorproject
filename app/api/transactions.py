"""
Transaction Monitoring API Endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.schemas import (
    TransactionRecord,
    TransactionListResponse,
    RiskLevel,
    PaymentMethod
)
from app.mock_data import (
    get_all_transactions,
    get_transaction_by_id,
    get_recent_transactions
)
from app.config import ErrorCodes

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get(
    "",
    response_model=TransactionListResponse,
    summary="List Transactions",
    description="""
    List all transactions with optional filtering.
    
    Supports filtering by:
    - Risk level (low, medium, high)
    - Payment method (card, upi, netbanking)
    - Merchant ID
    - Decision type
    - Pagination
    """
)
async def list_transactions(
    risk_level: Optional[str] = Query(None, description="Filter by risk level (LOW, MEDIUM, HIGH)"),
    payment_method: Optional[str] = Query(None, description="Filter by payment method (CARD, UPI, NETBANKING)"),
    merchant_id: Optional[str] = Query(None, description="Filter by merchant ID"),
    decision: Optional[str] = Query(None, description="Filter by decision (ALLOW, MONITOR, REQUIRE_REVIEW, BLOCK_DEMO_PAYMENT)"),
    min_amount: Optional[float] = Query(None, ge=0, description="Minimum transaction amount"),
    max_amount: Optional[float] = Query(None, ge=0, description="Maximum transaction amount"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
):
    """
    Get paginated list of transactions with optional filters
    """
    
    transactions = get_all_transactions()
    
    # Apply filters
    if risk_level:
        risk_level_upper = risk_level.upper()
        transactions = [t for t in transactions if t.risk_level.value == risk_level_upper]
    
    if payment_method:
        payment_method_upper = payment_method.upper()
        transactions = [t for t in transactions if t.method.value == payment_method_upper]
    
    if merchant_id:
        transactions = [t for t in transactions if t.merchant_id == merchant_id]
    
    if decision:
        decision_upper = decision.upper()
        transactions = [t for t in transactions if t.decision.value == decision_upper]
    
    if min_amount is not None:
        transactions = [t for t in transactions if t.amount >= min_amount]
    
    if max_amount is not None:
        transactions = [t for t in transactions if t.amount <= max_amount]
    
    total = len(transactions)
    
    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_transactions = transactions[start_idx:end_idx]
    
    return TransactionListResponse(
        transactions=paginated_transactions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get(
    "/recent",
    response_model=list[TransactionRecord],
    summary="Get Recent Transactions",
    description="""
    Get most recent transactions for the risk feed.
    
    Returns the latest transactions sorted by timestamp descending.
    Useful for real-time monitoring dashboards.
    """
)
async def get_recent_transactions_endpoint(
    limit: int = Query(20, ge=1, le=100, description="Number of recent transactions to retrieve")
):
    """
    Get recent transactions
    """
    
    return get_recent_transactions(limit=limit)


@router.get(
    "/{transaction_id}",
    response_model=TransactionRecord,
    summary="Get Transaction Details",
    description="""
    Retrieve detailed information about a specific transaction.
    
    Includes:
    - Complete risk assessment
    - Evidence signals
    - Decision rationale
    - Merchant information
    """
)
async def get_transaction(transaction_id: str):
    """
    Get transaction by ID
    """
    
    transaction = get_transaction_by_id(transaction_id)
    
    if not transaction:
        raise HTTPException(
            status_code=404,
            detail={
                "error": ErrorCodes.TRANSACTION_NOT_FOUND,
                "message": f"Transaction with ID '{transaction_id}' not found"
            }
        )
    
    return transaction


@router.get(
    "/merchant/{merchant_id}/history",
    response_model=TransactionListResponse,
    summary="Get Merchant Transaction History",
    description="""
    Get transaction history for a specific merchant.
    
    Useful for understanding merchant transaction patterns and risk trends.
    """
)
async def get_merchant_transactions(
    merchant_id: str,
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=100, description="Items per page")
):
    """
    Get transactions for a specific merchant
    """
    
    transactions = get_all_transactions()
    merchant_transactions = [t for t in transactions if t.merchant_id == merchant_id]
    
    total = len(merchant_transactions)
    
    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_transactions = merchant_transactions[start_idx:end_idx]
    
    return TransactionListResponse(
        transactions=paginated_transactions,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get(
    "/stats/summary",
    summary="Get Transaction Statistics",
    description="""
    Get summary statistics for transactions.
    
    Includes counts by risk level, payment method, and decision type.
    """
)
async def get_transaction_stats():
    """
    Get transaction summary statistics
    """
    
    transactions = get_all_transactions()
    
    # Risk level breakdown
    risk_breakdown = {
        "LOW": len([t for t in transactions if t.risk_level == RiskLevel.LOW]),
        "MEDIUM": len([t for t in transactions if t.risk_level == RiskLevel.MEDIUM]),
        "HIGH": len([t for t in transactions if t.risk_level == RiskLevel.HIGH])
    }
    
    # Payment method breakdown
    payment_breakdown = {
        "CARD": len([t for t in transactions if t.method == PaymentMethod.CARD]),
        "UPI": len([t for t in transactions if t.method == PaymentMethod.UPI]),
        "NETBANKING": len([t for t in transactions if t.method == PaymentMethod.NETBANKING])
    }
    
    # Decision breakdown
    decision_breakdown = {}
    for txn in transactions:
        decision_value = txn.decision.value
        decision_breakdown[decision_value] = decision_breakdown.get(decision_value, 0) + 1
    
    # Amount statistics
    amounts = [t.amount for t in transactions]
    total_volume = sum(amounts)
    avg_amount = total_volume / len(amounts) if amounts else 0
    
    return {
        "total_transactions": len(transactions),
        "total_volume_inr": round(total_volume, 2),
        "average_amount_inr": round(avg_amount, 2),
        "risk_breakdown": risk_breakdown,
        "payment_method_breakdown": payment_breakdown,
        "decision_breakdown": decision_breakdown
    }
