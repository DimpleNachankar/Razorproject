#!/bin/bash
# Test runner script for TRUSTSHIELD API

echo "=========================================="
echo "TRUSTSHIELD API Test Suite"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run tests
echo "Running tests..."
pytest

echo ""
echo "=========================================="
echo "Test run complete!"
echo "=========================================="
