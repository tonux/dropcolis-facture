#!/bin/bash

# Facture Generator Runner Script
# This script runs the facture generator with proper error handling

echo "Facture Generator - Starting..."
echo "================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $python_version is installed, but Python $required_version or higher is required"
    exit 1
fi

echo "✓ Python $python_version detected"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment found, activating..."
    source venv/bin/activate
else
    echo "⚠ No virtual environment found"
    echo "Consider creating one with: python3 -m venv venv"
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import requests, jinja2, weasyprint" &> /dev/null; then
    echo "⚠ Some dependencies are missing"
    echo "Installing requirements..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install requirements"
        echo "Please check the error messages above and install manually:"
        echo "pip install -r requirements.txt"
        exit 1
    fi
fi

echo "✓ Dependencies check passed"

# Run the facture generator
echo ""
echo "Running Facture Generator..."
echo "================================"

python3 generate_facture.py

# Check exit code
exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo ""
    echo "✓ Facture Generator completed successfully!"
elif [ $exit_code -eq 1 ]; then
    echo ""
    echo "⚠ Facture Generator completed with warnings"
else
    echo ""
    echo "✗ Facture Generator failed with errors"
fi

exit $exit_code
