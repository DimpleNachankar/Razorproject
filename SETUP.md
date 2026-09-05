# TRUSTSHIELD Backend Setup Guide

Complete setup and deployment guide for the TRUSTSHIELD FastAPI backend.

---

## Quick Start

### 1. Prerequisites

- **Python**: 3.9 or higher
- **pip**: Latest version
- **Virtual environment**: Recommended

### 2. Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (optional for demo mode)
# nano .env
```

### 4. Run Development Server

```bash
# Using the run script (recommended)
./run_dev.sh

# OR manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access API

- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Running Tests

```bash
# Using the test script
./run_tests.sh

# OR manually
pytest

# With coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_merchants.py -v

# Run tests matching pattern
pytest -k "merchant" -v
```

---

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration & settings
│   ├── schemas.py                 # Pydantic models
│   ├── mock_data.py               # Demo data layer
│   ├── risk_engine.py             # Risk calculation engine
│   ├── middleware.py              # CORS, logging, error handling
│   └── api/
│       ├── __init__.py
│       ├── merchants.py           # Merchant endpoints
│       ├── transactions.py        # Transaction endpoints
│       ├── checkout.py            # Checkout evaluation
│       ├── simulator.py           # Risk simulator
│       ├── evidence.py            # Signal catalog
│       ├── analytics.py           # Analytics
│       ├── models.py              # ML model status
│       └── dashboard.py           # Dashboard metrics
├── tests/
│   ├── conftest.py                # Test fixtures
│   ├── test_*.py                  # Test modules
│   └── ...
├── requirements.txt
├── pytest.ini
├── .env
├── .env.example
├── README.md
├── SETUP.md
└── run_dev.sh
```

---

## API Endpoints Overview

### Health & Status
- `GET /health` - Health check
- `GET /ping` - Ping endpoint
- `GET /api/info` - API information
- `GET /api/v1/status` - System status

### Dashboard
- `GET /api/v1/dashboard/overview` - Dashboard metrics
- `GET /api/v1/dashboard/system-health` - System health
- `GET /api/v1/dashboard/activity-feed` - Recent activity
- `GET /api/v1/dashboard/alerts` - Active alerts
- `GET /api/v1/dashboard/quick-stats` - Quick statistics

### Merchants
- `POST /api/v1/merchants/analyze` - Analyze merchant domain
- `GET /api/v1/merchants` - List merchants
- `GET /api/v1/merchants/{id}` - Get merchant by ID
- `GET /api/v1/merchants/domain/{domain}` - Get by domain

### Transactions
- `GET /api/v1/transactions` - List transactions
- `GET /api/v1/transactions/{id}` - Get transaction details
- `GET /api/v1/transactions/recent` - Recent transactions
- `GET /api/v1/transactions/merchant/{id}/history` - Merchant history
- `GET /api/v1/transactions/stats/summary` - Transaction stats

### Checkout
- `POST /api/v1/checkout/evaluate` - Evaluate checkout risk
- `POST /api/v1/checkout/simulate-payment` - Simulate payment

### Simulator
- `POST /api/v1/simulator/calculate` - Calculate risk score
- `GET /api/v1/simulator/presets` - Get simulator presets
- `POST /api/v1/simulator/batch-calculate` - Batch calculation

### Evidence
- `GET /api/v1/evidence/signals` - Get signal catalog
- `GET /api/v1/evidence/signals/{id}` - Get signal details
- `GET /api/v1/evidence/categories` - Signal categories
- `GET /api/v1/evidence/impact-analysis` - Impact analysis
- `GET /api/v1/evidence/provenance` - Provenance info

### Analytics
- `GET /api/v1/analytics/overview` - Analytics overview
- `GET /api/v1/analytics/trends` - Risk trends
- `GET /api/v1/analytics/merchant-risk-distribution` - Merchant risk
- `GET /api/v1/analytics/payment-method-analysis` - Payment analysis
- `GET /api/v1/analytics/velocity-patterns` - Velocity patterns

### Models
- `GET /api/v1/models/status` - Model status
- `GET /api/v1/models/architecture` - Model architecture
- `GET /api/v1/models/evaluation` - Evaluation specs
- `GET /api/v1/models/feature-importance` - Feature importance

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Runtime environment | `development` |
| `DEMO_MODE` | Enable demo mode | `true` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000,...` |
| `AUTO_ALLOW_THRESHOLD` | Auto-allow risk score threshold | `30` |
| `REQUIRE_REVIEW_THRESHOLD` | Review threshold | `60` |
| `AUTO_BLOCK_THRESHOLD` | Auto-block threshold | `85` |
| `VERBOSE_LOGGING` | Enable verbose logging | `true` |

---

## Development

### Adding New Endpoints

1. Create route handler in `app/api/`
2. Add router to `app/main.py`
3. Add Pydantic schemas to `app/schemas.py` if needed
4. Write tests in `tests/`

### Code Style

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/
```

### Running in Production Mode

```bash
# Use gunicorn with uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Module Import Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### CORS Errors

- Check `ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL is included
- Restart server after changes

---

## Demo Mode Features

✅ Mock merchant and transaction data
✅ Deterministic risk scoring
✅ No external API calls
✅ No real payment processing
✅ Safe for demos and testing

---

## Next Steps

1. **Integrate with Frontend**: Update frontend API base URL to `http://localhost:8000`
2. **Test API**: Use Swagger UI at `/docs` to test endpoints
3. **Run Tests**: Execute `./run_tests.sh` to verify all tests pass
4. **Deploy**: Follow deployment guide for production setup

---

## Support

For issues or questions:
- Check API documentation at `/docs`
- Review test cases in `tests/`
- See main README.md for project overview

---

**Built for Razorpay AI Buildathon 2026** 🚀
