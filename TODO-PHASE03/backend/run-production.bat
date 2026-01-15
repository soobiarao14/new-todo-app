@echo off
REM Script to run the backend in production mode (for local testing)

echo ========================================
echo Starting Backend in PRODUCTION mode
echo ========================================
echo.
echo WARNING: This will use production configuration!
echo Make sure .env.production is properly configured.
echo.

REM Set environment to production
set APP_ENV=production

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting uvicorn server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

REM Start the server (no reload in production mode)
uvicorn src.main:app --host 0.0.0.0 --port 8000
