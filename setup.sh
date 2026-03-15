#!/bin/bash

# CanConnect Streamlit Setup Script for macOS/Linux

echo ""
echo "==================================="
echo "CanConnect Streamlit Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org"
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

echo ""
echo "[2/4] Creating virtual environment..."
python3 -m venv venv

echo ""
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[4/4] Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "3. Make sure PostgreSQL is running before starting the app"
echo ""
