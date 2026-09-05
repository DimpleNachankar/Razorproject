# TRUSTSHIELD Backend API

**AI-Powered Merchant & Real-Time Payment Risk Intelligence Platform**

Built for Razorpay AI Buildathon 2026.

---

## Overview

TRUSTSHIELD is a complementary merchant and transaction risk intelligence layer that provides:

- **Merchant Risk Assessment**: Domain analysis, identity verification, policy detection
- **Transaction Monitoring**: Real-time payment risk evaluation with velocity tracking
- **Evidence-Based Decisions**: Structured signal catalog with provenance tracking
- **Risk Scoring**: 0-100 risk score with confidence levels
- **Actionable Recommendations**: ALLOW, MONITOR, REQUIRE_REVIEW, BLOCK_DEMO_PAYMENT, INSUFFICIENT_EVIDENCE

---

## Technology Stack

- **Framework**: FastAPI 0.109.0
- **Python**: 3.9+
- **Validation**: Pydantic 2.5.3
- **Server**: Uvicorn (ASGI)

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration & settings
│   ├── schemas.py                 # Pydantic data models
│   ├── mock_data.py               # Demo data layer
│   ├── risk_engine.py             # Mock risk calculation engine
│   ├── middleware.py              # CORS, logging, error handling
│   └── api/
│       ├── __init__.py
│       ├── merchants.py           # Merchant analysis endpoints
│       ├── transactions.py        # Transaction monitoring endpoints
│       ├── checkout.py            # Checkout risk evaluation
│       ├── simulator.py           # Risk simulator
│       ├── evidence.py            # Evidence & signal library
│       ├── analytics.py           # Analytics & metrics
│       ├── models.py              # ML model status
│       └── dashboard.py           # Dashboard overview
├── tests/
│   ├── __init__.py
│   ├── test_merchants.py
│   ├── test_transactions.py
│   └── test_risk_engine.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

---

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API Documentation

Once the server is running, access:

- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## API Endpoints

### Dashboard
- `GET /api/v1/dashboard/overview` - System overview metrics

### Merchants
- `POST /api/v1/merchants/analyze` - Analyze merchant domain
- `GET /api/v1/merchants` - List merchants with filters
- `GET /api/v1/merchants/{merchant_id}` - Get merchant details

### Transactions
- `GET /api/v1/transactions` - List transactions with filters
- `GET /api/v1/transactions/{transaction_id}` - Get transaction details
- `GET /api/v1/transactions/recent` - Get recent risk events

### Checkout
- `POST /api/v1/checkout/evaluate` - Evaluate checkout risk

### Simulator
- `POST /api/v1/simulator/calculate` - Calculate risk score dynamically

### Evidence
- `GET /api/v1/evidence/signals` - Get signal catalog
- `GET /api/v1/evidence/signals/{signal_id}` - Get signal details

### Analytics
- `GET /api/v1/analytics/overview` - Analytics overview
- `GET /api/v1/analytics/trends` - Risk trends over time

### Models
- `GET /api/v1/models/status` - ML model performance specs

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_merchants.py -v
```

---

## Demo Mode

The backend runs in **DEMO MODE** with:
- ✅ Mock merchant and transaction data
- ✅ Deterministic risk calculation
- ✅ No external API calls
- ✅ No real payment processing
- ✅ Client-safe CORS configuration

---

## Risk Decision Logic

| Risk Score | Risk Level | Decision |
|------------|------------|----------|
| 0-30 | LOW | ALLOW |
| 31-60 | MEDIUM | MONITOR |
| 61-84 | HIGH | REQUIRE_REVIEW |
| 85-100 | CRITICAL | BLOCK_DEMO_PAYMENT |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment | `development` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |
| `DEMO_MODE` | Enable demo mode | `true` |
| `AUTO_ALLOW_THRESHOLD` | Auto-allow threshold | `30` |
| `REQUIRE_REVIEW_THRESHOLD` | Review threshold | `60` |
| `AUTO_BLOCK_THRESHOLD` | Auto-block threshold | `85` |

---

## Architecture Notes

### Complementary Risk Layer

TRUSTSHIELD **does NOT replace** Razorpay's core fraud detection. It enriches pre-authorization decisions with:

1. **Merchant Website Intelligence**: Domain age, SSL, policy detection
2. **Entity Provenance**: Business registration, contact verification
3. **Transaction Velocity**: Per-merchant, per-card, per-device tracking
4. **Explainable Signals**: Structured evidence with confidence scores

### Mock Risk Engine

The current engine uses deterministic heuristics:

- Domain age weighting
- SSL/TLS validation scoring
- Policy presence detection
- Transaction velocity limits
- Payment method risk profiles

**Future**: Machine learning models (Random Forest, XGBoost) trained on historical settlement data.

---

## Disclaimer

This is a **student prototype** for the Razorpay AI Buildathon 2026.

- ⚠️ **NO REAL PAYMENTS**: All payment processing is simulated
- ⚠️ **DEMO DATA ONLY**: Mock merchants and transactions
- ⚠️ **NOT PRODUCTION-READY**: No database, authentication, or deployment

---

## License

Educational prototype - Razorpay AI Buildathon 2026

---

## Contact

Built by: [Your Name]
Event: Razorpay AI Buildathon 2026
