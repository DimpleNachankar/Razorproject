#!/bin/bash
# Development server launcher for TRUSTSHIELD API

echo "=========================================="
echo "TRUSTSHIELD API - Development Server"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run setup:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found, using defaults..."
    cp .env.example .env
fi

echo "✓ Starting server..."
echo ""
echo "=========================================="
echo "Server will start at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Alternative Docs: http://localhost:8000/redoc"
echo "=========================================="
echo ""

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
