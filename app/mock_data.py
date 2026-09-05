"""
Mock Data Layer for TRUSTSHIELD API
Realistic merchant and transaction records for demo mode
"""

from datetime import datetime, timedelta
from typing import List, Optional
import random
from app.schemas import (
    MerchantRecord,
    TransactionRecord,
    EvidenceSignal,
    RiskLevel,
    RiskDecision,
    SignalCategory,
    SignalProvenance,
    ImpactLevel,
    PaymentMethod
)
from app.config import BusinessCategories


# ============================================================================
# MOCK MERCHANTS DATA
# ============================================================================

MOCK_MERCHANTS_DATA = [
    # LOW RISK MERCHANTS
    {
        "id": "merch_001",
        "name": "UrbanNest Handicrafts",
        "domain": "urbannest.in",
        "category": BusinessCategories.HANDICRAFTS,
        "age_days": 730,
        "risk_score": 18.0,
        "risk_level": RiskLevel.LOW,
        "decision": RiskDecision.ALLOW,
        "confidence": 92.0,
        "refund_policy_detected": True,
        "contact_score": "Complete",
        "signals": [
            {
                "id": "sig_merch001_001",
                "category": SignalCategory.WEBSITE,
                "title": "Domain Age",
                "value": "730 days (2 years)",
                "impact": ImpactLevel.LOW,
                "confidence": 98.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Established domain with good historical presence"
            },
            {
                "id": "sig_merch001_002",
                "category": SignalCategory.WEBSITE,
                "title": "SSL Certificate",
                "value": "Valid (Let's Encrypt, expires 2026-12-15)",
                "impact": ImpactLevel.LOW,
                "confidence": 100.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Valid SSL/TLS certificate detected"
            },
            {
                "id": "sig_merch001_003",
                "category": SignalCategory.IDENTITY,
                "title": "Refund Policy",
                "value": "Detected: 30-day return policy",
                "impact": ImpactLevel.LOW,
                "confidence": 85.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "Clear refund and cancellation policy found"
            },
            {
                "id": "sig_merch001_004",
                "category": SignalCategory.IDENTITY,
                "title": "Contact Information",
                "value": "Complete: Email, Phone, Physical Address",
                "impact": ImpactLevel.LOW,
                "confidence": 90.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "Comprehensive contact details available"
            }
        ]
    },
    {
        "id": "merch_002",
        "name": "BookHaven India",
        "domain": "bookhaven.co.in",
        "category": BusinessCategories.BOOKS,
        "age_days": 1095,
        "risk_score": 12.0,
        "risk_level": RiskLevel.LOW,
        "decision": RiskDecision.ALLOW,
        "confidence": 95.0,
        "refund_policy_detected": True,
        "contact_score": "Complete",
        "signals": []
    },
    {
        "id": "merch_003",
        "name": "FreshMart Groceries",
        "domain": "freshmart.in",
        "category": BusinessCategories.GROCERIES,
        "age_days": 456,
        "risk_score": 22.0,
        "risk_level": RiskLevel.LOW,
        "decision": RiskDecision.ALLOW,
        "confidence": 88.0,
        "refund_policy_detected": True,
        "contact_score": "Complete",
        "signals": []
    },
    
    # MEDIUM RISK MERCHANTS
    {
        "id": "merch_004",
        "name": "TechMart Gadgets",
        "domain": "techmart-india.com",
        "category": BusinessCategories.ELECTRONICS,
        "age_days": 125,
        "risk_score": 54.0,
        "risk_level": RiskLevel.MEDIUM,
        "decision": RiskDecision.MONITOR,
        "confidence": 76.0,
        "refund_policy_detected": False,
        "contact_score": "Partial",
        "signals": [
            {
                "id": "sig_merch004_001",
                "category": SignalCategory.WEBSITE,
                "title": "Domain Age",
                "value": "125 days (4 months)",
                "impact": ImpactLevel.MEDIUM,
                "confidence": 95.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Relatively new domain, moderate risk"
            },
            {
                "id": "sig_merch004_002",
                "category": SignalCategory.IDENTITY,
                "title": "Refund Policy",
                "value": "Not found",
                "impact": ImpactLevel.MEDIUM,
                "confidence": 80.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "No clear refund/cancellation policy detected"
            },
            {
                "id": "sig_merch004_003",
                "category": SignalCategory.IDENTITY,
                "title": "Contact Information",
                "value": "Partial: Email only, no phone",
                "impact": ImpactLevel.MEDIUM,
                "confidence": 85.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "Incomplete contact information"
            },
            {
                "id": "sig_merch004_004",
                "category": SignalCategory.WEBSITE,
                "title": "SSL Certificate",
                "value": "Valid",
                "impact": ImpactLevel.LOW,
                "confidence": 100.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Valid SSL certificate present"
            }
        ]
    },
    {
        "id": "merch_005",
        "name": "StyleHub Fashion",
        "domain": "stylehub-fashion.shop",
        "category": BusinessCategories.FASHION,
        "age_days": 89,
        "risk_score": 48.0,
        "risk_level": RiskLevel.MEDIUM,
        "decision": RiskDecision.MONITOR,
        "confidence": 70.0,
        "refund_policy_detected": True,
        "contact_score": "Partial",
        "signals": []
    },
    
    # HIGH RISK MERCHANTS
    {
        "id": "merch_006",
        "name": "SwiftDrop Electronics",
        "domain": "swiftdrop-deals.shop",
        "category": BusinessCategories.ELECTRONICS,
        "age_days": 14,
        "risk_score": 87.0,
        "risk_level": RiskLevel.HIGH,
        "decision": RiskDecision.BLOCK_DEMO_PAYMENT,
        "confidence": 85.0,
        "refund_policy_detected": False,
        "contact_score": "Missing",
        "signals": [
            {
                "id": "sig_merch006_001",
                "category": SignalCategory.WEBSITE,
                "title": "Domain Age",
                "value": "14 days",
                "impact": ImpactLevel.HIGH,
                "confidence": 98.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Very new domain, high fraud risk indicator"
            },
            {
                "id": "sig_merch006_002",
                "category": SignalCategory.WEBSITE,
                "title": "SSL Certificate",
                "value": "Self-signed / Invalid",
                "impact": ImpactLevel.HIGH,
                "confidence": 95.0,
                "provenance": SignalProvenance.DNS_SCAN,
                "description": "Invalid or self-signed SSL certificate"
            },
            {
                "id": "sig_merch006_003",
                "category": SignalCategory.IDENTITY,
                "title": "Refund Policy",
                "value": "Not found",
                "impact": ImpactLevel.HIGH,
                "confidence": 90.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "No refund policy detected"
            },
            {
                "id": "sig_merch006_004",
                "category": SignalCategory.IDENTITY,
                "title": "Contact Information",
                "value": "Missing",
                "impact": ImpactLevel.HIGH,
                "confidence": 92.0,
                "provenance": SignalProvenance.CONTENT_EVAL,
                "description": "No contact information available"
            },
            {
                "id": "sig_merch006_005",
                "category": SignalCategory.IDENTITY,
                "title": "Entity Verification",
                "value": "No business registration found",
                "impact": ImpactLevel.HIGH,
                "confidence": 80.0,
                "provenance": SignalProvenance.CONSORTIUM_MOCK,
                "description": "Unable to verify business entity"
            }
        ]
    },
    {
        "id": "merch_007",
        "name": "MegaDeal SuperStore",
        "domain": "megadeal-store.xyz",
        "category": BusinessCategories.ELECTRONICS,
        "age_days": 7,
        "risk_score": 92.0,
        "risk_level": RiskLevel.HIGH,
        "decision": RiskDecision.BLOCK_DEMO_PAYMENT,
        "confidence": 88.0,
        "refund_policy_detected": False,
        "contact_score": "Missing",
        "signals": []
    },
    {
        "id": "merch_008",
        "name": "QuickFashion Outlet",
        "domain": "quickfashion-outlet.online",
        "category": BusinessCategories.FASHION,
        "age_days": 21,
        "risk_score": 79.0,
        "risk_level": RiskLevel.HIGH,
        "decision": RiskDecision.REQUIRE_REVIEW,
        "confidence": 82.0,
        "refund_policy_detected": False,
        "contact_score": "Partial",
        "signals": []
    },
    
    # Additional merchants for variety
    {
        "id": "merch_009",
        "name": "WellnessPharm Healthcare",
        "domain": "wellnesspharm.co.in",
        "category": BusinessCategories.PHARMACEUTICALS,
        "age_days": 912,
        "risk_score": 15.0,
        "risk_level": RiskLevel.LOW,
        "decision": RiskDecision.ALLOW,
        "confidence": 94.0,
        "refund_policy_detected": True,
        "contact_score": "Complete",
        "signals": []
    },
    {
        "id": "merch_010",
        "name": "EduPro Learning",
        "domain": "edupro-learning.in",
        "category": BusinessCategories.EDUCATION,
        "age_days": 645,
        "risk_score": 20.0,
        "risk_level": RiskLevel.LOW,
        "decision": RiskDecision.ALLOW,
        "confidence": 90.0,
        "refund_policy_detected": True,
        "contact_score": "Complete",
        "signals": []
    }
]


# ============================================================================
# MOCK TRANSACTIONS DATA
# ============================================================================

def generate_mock_transactions(count: int = 50) -> List[dict]:
    """Generate realistic mock transaction data"""
    
    transactions = []
    base_time = datetime.utcnow()
    
    # Sample data for variety
    merchants = [m["id"] for m in MOCK_MERCHANTS_DATA]
    merchant_names = {m["id"]: m["name"] for m in MOCK_MERCHANTS_DATA}
    merchant_risk_levels = {m["id"]: m["risk_level"] for m in MOCK_MERCHANTS_DATA}
    
    payment_methods = [PaymentMethod.CARD, PaymentMethod.UPI, PaymentMethod.NETBANKING]
    locations = [
        "Mumbai, Maharashtra", "Bangalore, Karnataka", "Delhi, Delhi",
        "Pune, Maharashtra", "Hyderabad, Telangana", "Chennai, Tamil Nadu",
        "Kolkata, West Bengal", "Ahmedabad, Gujarat", "Jaipur, Rajasthan"
    ]
    
    for i in range(count):
        merchant_id = random.choice(merchants)
        merchant_name = merchant_names[merchant_id]
        merchant_risk = merchant_risk_levels[merchant_id]
        
        # Generate transaction details
        amount = round(random.choice([
            random.uniform(100, 5000),    # Small purchases
            random.uniform(5000, 25000),  # Medium purchases
            random.uniform(25000, 100000) # Large purchases
        ]), 2)
        
        payment_method = random.choice(payment_methods)
        velocity = random.choices([1, 2, 3, 4, 5, 8, 12], weights=[50, 20, 15, 8, 4, 2, 1])[0]
        timestamp = base_time - timedelta(hours=random.randint(0, 72), minutes=random.randint(0, 59))
        
        # Calculate risk based on factors
        base_risk = 10 if merchant_risk == RiskLevel.LOW else (40 if merchant_risk == RiskLevel.MEDIUM else 70)
        
        # Amount factor
        if amount > 50000:
            amount_risk = 20
        elif amount > 25000:
            amount_risk = 12
        elif amount > 10000:
            amount_risk = 6
        else:
            amount_risk = 0
        
        # Velocity factor
        velocity_risk = max(0, (velocity - 3) * 8)
        
        # Payment method factor
        method_risk = 5 if payment_method == PaymentMethod.CARD else (3 if payment_method == PaymentMethod.UPI else 2)
        
        # Calculate final risk score
        risk_score = min(100, base_risk + amount_risk + velocity_risk + method_risk + random.uniform(-5, 5))
        risk_score = max(0, round(risk_score, 1))
        
        # Determine risk level and decision
        if risk_score < 30:
            risk_level = RiskLevel.LOW
            decision = RiskDecision.ALLOW
        elif risk_score < 60:
            risk_level = RiskLevel.MEDIUM
            decision = RiskDecision.MONITOR
        elif risk_score < 85:
            risk_level = RiskLevel.HIGH
            decision = RiskDecision.REQUIRE_REVIEW
        else:
            risk_level = RiskLevel.HIGH
            decision = RiskDecision.BLOCK_DEMO_PAYMENT
        
        # Generate transaction signals
        signals = []
        
        if amount > 50000:
            signals.append({
                "id": f"sig_txn{i:03d}_001",
                "category": SignalCategory.PAYMENT,
                "title": "High Transaction Amount",
                "value": f"₹{amount:,.2f}",
                "impact": ImpactLevel.HIGH,
                "confidence": 95.0,
                "provenance": SignalProvenance.PAYMENT_GATEWAY,
                "description": "Transaction amount exceeds ₹50,000 threshold"
            })
        
        if velocity > 5:
            signals.append({
                "id": f"sig_txn{i:03d}_002",
                "category": SignalCategory.VELOCITY,
                "title": "High Transaction Velocity",
                "value": f"{velocity} transactions in 1 hour",
                "impact": ImpactLevel.HIGH,
                "confidence": 90.0,
                "provenance": SignalProvenance.VELOCITY_TRACKER,
                "description": "Unusual transaction frequency detected"
            })
        
        if payment_method == PaymentMethod.CARD:
            signals.append({
                "id": f"sig_txn{i:03d}_003",
                "category": SignalCategory.PAYMENT,
                "title": "Card Payment",
                "value": "Visa ending in " + str(random.randint(1000, 9999)),
                "impact": ImpactLevel.LOW,
                "confidence": 100.0,
                "provenance": SignalProvenance.PAYMENT_GATEWAY,
                "description": "Card payment detected - standard risk profile"
            })
        
        # Build transaction record
        transaction = {
            "id": f"txn_20260903_{i:04d}",
            "merchant_id": merchant_id,
            "merchant_name": merchant_name,
            "amount": amount,
            "currency": "INR",
            "method": payment_method,
            "card_last4": str(random.randint(1000, 9999)) if payment_method == PaymentMethod.CARD else None,
            "upi_handle": f"user{random.randint(100,999)}@{random.choice(['okhdfcbank', 'paytm', 'googlepay'])}" if payment_method == PaymentMethod.UPI else None,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "decision": decision,
            "confidence": round(85 + random.uniform(-10, 10), 1),
            "velocity_1h": velocity,
            "ip_location": random.choice(locations),
            "device_fingerprint": f"fp_{random.randint(100000, 999999)}",
            "signals": signals,
            "timestamp": timestamp.isoformat()
        }
        
        transactions.append(transaction)
    
    # Sort by timestamp descending (most recent first)
    transactions.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return transactions


# ============================================================================
# EVIDENCE SIGNAL CATALOG
# ============================================================================

SIGNAL_CATALOG = [
    {
        "id": "sig_catalog_001",
        "category": SignalCategory.WEBSITE,
        "title": "Domain Age",
        "value": "Variable",
        "impact": ImpactLevel.HIGH,
        "confidence": 95.0,
        "provenance": SignalProvenance.DNS_SCAN,
        "description": "Age of domain registration. Newer domains (< 30 days) indicate higher fraud risk."
    },
    {
        "id": "sig_catalog_002",
        "category": SignalCategory.WEBSITE,
        "title": "SSL/TLS Certificate",
        "value": "Valid/Invalid",
        "impact": ImpactLevel.MEDIUM,
        "confidence": 100.0,
        "provenance": SignalProvenance.DNS_SCAN,
        "description": "Presence and validity of SSL certificate for secure communications."
    },
    {
        "id": "sig_catalog_003",
        "category": SignalCategory.IDENTITY,
        "title": "Refund Policy",
        "value": "Detected/Not Found",
        "impact": ImpactLevel.MEDIUM,
        "confidence": 80.0,
        "provenance": SignalProvenance.CONTENT_EVAL,
        "description": "Presence of clear refund and cancellation policy on merchant website."
    },
    {
        "id": "sig_catalog_004",
        "category": SignalCategory.IDENTITY,
        "title": "Contact Information",
        "value": "Complete/Partial/Missing",
        "impact": ImpactLevel.MEDIUM,
        "confidence": 85.0,
        "provenance": SignalProvenance.CONTENT_EVAL,
        "description": "Availability of contact details: email, phone, physical address."
    },
    {
        "id": "sig_catalog_005",
        "category": SignalCategory.IDENTITY,
        "title": "Business Registration",
        "value": "Verified/Not Found",
        "impact": ImpactLevel.HIGH,
        "confidence": 75.0,
        "provenance": SignalProvenance.CONSORTIUM_MOCK,
        "description": "Verification of business entity registration with government databases."
    },
    {
        "id": "sig_catalog_006",
        "category": SignalCategory.VELOCITY,
        "title": "Transaction Velocity",
        "value": "Transactions per hour",
        "impact": ImpactLevel.HIGH,
        "confidence": 90.0,
        "provenance": SignalProvenance.VELOCITY_TRACKER,
        "description": "Frequency of transactions from same card/account in short time window."
    },
    {
        "id": "sig_catalog_007",
        "category": SignalCategory.PAYMENT,
        "title": "Transaction Amount",
        "value": "Amount in INR",
        "impact": ImpactLevel.MEDIUM,
        "confidence": 100.0,
        "provenance": SignalProvenance.PAYMENT_GATEWAY,
        "description": "Transaction amount relative to merchant average and customer history."
    },
    {
        "id": "sig_catalog_008",
        "category": SignalCategory.PAYMENT,
        "title": "Failed Payment Attempts",
        "value": "Count in 15 minutes",
        "impact": ImpactLevel.HIGH,
        "confidence": 95.0,
        "provenance": SignalProvenance.PAYMENT_GATEWAY,
        "description": "Number of failed payment attempts in recent time window."
    },
    {
        "id": "sig_catalog_009",
        "category": SignalCategory.NETWORK,
        "title": "IP Geolocation",
        "value": "City, State",
        "impact": ImpactLevel.LOW,
        "confidence": 80.0,
        "provenance": SignalProvenance.DEVICE_FINGERPRINT,
        "description": "Geographic location of customer IP address."
    },
    {
        "id": "sig_catalog_010",
        "category": SignalCategory.NETWORK,
        "title": "Device Fingerprint",
        "value": "Hash identifier",
        "impact": ImpactLevel.MEDIUM,
        "confidence": 85.0,
        "provenance": SignalProvenance.DEVICE_FINGERPRINT,
        "description": "Unique device identifier for tracking repeat offenders."
    }
]


# ============================================================================
# DATA ACCESS FUNCTIONS
# ============================================================================

def get_all_merchants() -> List[MerchantRecord]:
    """Get all mock merchants"""
    merchants = []
    for data in MOCK_MERCHANTS_DATA:
        signals = [EvidenceSignal(**sig) for sig in data.get("signals", [])]
        merchant_data = data.copy()
        merchant_data["signals"] = signals
        merchant_data["created_at"] = datetime.utcnow() - timedelta(days=data["age_days"])
        merchant_data["last_evaluated"] = datetime.utcnow()
        merchants.append(MerchantRecord(**merchant_data))
    return merchants


def get_merchant_by_id(merchant_id: str) -> Optional[MerchantRecord]:
    """Get merchant by ID"""
    for merchant in get_all_merchants():
        if merchant.id == merchant_id:
            return merchant
    return None


def get_merchant_by_domain(domain: str) -> Optional[MerchantRecord]:
    """Get merchant by domain"""
    domain = domain.lower().strip()
    for merchant in get_all_merchants():
        if merchant.domain.lower() == domain:
            return merchant
    return None


def get_all_transactions() -> List[TransactionRecord]:
    """Get all mock transactions"""
    transaction_data = generate_mock_transactions(100)
    transactions = []
    for data in transaction_data:
        signals = [EvidenceSignal(**sig) for sig in data.get("signals", [])]
        txn_data = data.copy()
        txn_data["signals"] = signals
        txn_data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        transactions.append(TransactionRecord(**txn_data))
    return transactions


def get_transaction_by_id(transaction_id: str) -> Optional[TransactionRecord]:
    """Get transaction by ID"""
    for transaction in get_all_transactions():
        if transaction.id == transaction_id:
            return transaction
    return None


def get_recent_transactions(limit: int = 20) -> List[TransactionRecord]:
    """Get most recent transactions"""
    all_transactions = get_all_transactions()
    return sorted(all_transactions, key=lambda x: x.timestamp, reverse=True)[:limit]


def get_signal_catalog() -> List[EvidenceSignal]:
    """Get all evidence signals in catalog"""
    return [EvidenceSignal(**sig) for sig in SIGNAL_CATALOG]


def get_signal_by_id(signal_id: str) -> Optional[EvidenceSignal]:
    """Get specific signal by ID"""
    for signal in get_signal_catalog():
        if signal.id == signal_id:
            return signal
    return None


# ============================================================================
# STATISTICS FUNCTIONS
# ============================================================================

def get_dashboard_stats() -> dict:
    """Get dashboard overview statistics"""
    transactions = get_all_transactions()
    merchants = get_all_merchants()
    
    total_transactions = len(transactions)
    total_volume = sum(txn.amount for txn in transactions)
    flagged = [txn for txn in transactions if txn.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH]]
    high_risk_merchants = [m for m in merchants if m.risk_level == RiskLevel.HIGH]
    review_needed = [txn for txn in transactions if txn.decision == RiskDecision.REQUIRE_REVIEW]
    
    return {
        "total_transactions": total_transactions,
        "total_volume_inr": round(total_volume, 2),
        "flagged_transactions": len(flagged),
        "flagged_percentage": round((len(flagged) / total_transactions * 100), 2) if total_transactions > 0 else 0,
        "high_risk_merchants": len(high_risk_merchants),
        "manual_review_rate": round((len(review_needed) / total_transactions * 100), 2) if total_transactions > 0 else 0
    }


def get_risk_distribution() -> dict:
    """Get risk level distribution"""
    transactions = get_all_transactions()
    
    low = len([t for t in transactions if t.risk_level == RiskLevel.LOW])
    medium = len([t for t in transactions if t.risk_level == RiskLevel.MEDIUM])
    high = len([t for t in transactions if t.risk_level == RiskLevel.HIGH])
    
    return {
        "low": low,
        "medium": medium,
        "high": high
    }


def get_decision_distribution() -> dict:
    """Get decision type distribution"""
    transactions = get_all_transactions()
    
    distribution = {}
    for decision in RiskDecision:
        count = len([t for t in transactions if t.decision == decision])
        distribution[decision.value] = count
    
    return distribution


def get_payment_method_breakdown() -> dict:
    """Get payment method breakdown"""
    transactions = get_all_transactions()
    
    breakdown = {}
    for method in PaymentMethod:
        count = len([t for t in transactions if t.method == method])
        breakdown[method.value] = count
    
    return breakdown


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    "get_all_merchants",
    "get_merchant_by_id",
    "get_merchant_by_domain",
    "get_all_transactions",
    "get_transaction_by_id",
    "get_recent_transactions",
    "get_signal_catalog",
    "get_signal_by_id",
    "get_dashboard_stats",
    "get_risk_distribution",
    "get_decision_distribution",
    "get_payment_method_breakdown"
]
