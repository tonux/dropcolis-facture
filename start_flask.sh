#!/bin/bash

# Start Flask Application Script
# This script starts the Flask API for facture generation

echo "Starting Flask Application for Facture Generation..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   Run: ./run.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if Flask is installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Flask..."
    pip install flask
fi

# Check if config.json exists
if [ ! -f "config.json" ]; then
    echo "❌ config.json not found. Please configure your API endpoints first."
    exit 1
fi

# Set Flask environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export PORT=5000

echo "🚀 Starting Flask application on port $PORT..."
echo "   Health check: http://localhost:$PORT/health"
echo "   API docs: http://localhost:$PORT/"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Start Flask application
python3 app.py
