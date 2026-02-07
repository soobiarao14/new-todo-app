@echo off
REM Script to run the backend in local development mode

echo ========================================
echo Starting Backend in LOCAL mode
echo ========================================
echo.

REM Set environment to local
set APP_ENV=local

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting uvicorn server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
