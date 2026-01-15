#!/bin/bash
# Script to run the backend in local development mode

echo "========================================"
echo "Starting Backend in LOCAL mode"
echo "========================================"
echo ""

# Set environment to local
export APP_ENV=local

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting uvicorn server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
