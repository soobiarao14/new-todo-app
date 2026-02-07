#!/bin/bash
# Script to run the backend in production mode (for local testing)

echo "========================================"
echo "Starting Backend in PRODUCTION mode"
echo "========================================"
echo ""
echo "WARNING: This will use production configuration!"
echo "Make sure .env.production is properly configured."
echo ""

# Set environment to production
export APP_ENV=production

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Starting uvicorn server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server (no reload in production mode)
uvicorn src.main:app --host 0.0.0.0 --port 8000
