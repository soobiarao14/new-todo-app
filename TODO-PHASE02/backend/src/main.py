"""
FastAPI application instance with CORS middleware and authentication.
Phase II Full-Stack Todo Application Backend.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv
from src.middleware.auth import AuthMiddleware
from src.middleware.error_handler import (
    global_exception_handler,
    validation_exception_handler,
    http_exception_handler,
)
from src.routes.auth import router as auth_router
from src.db import create_db_and_tables

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application - RESTful API with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Register exception handlers
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

# Configure CORS middleware (must be before auth middleware)
# IMPORTANT: In production, replace with actual frontend domain
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Content-Type"],
)

# Add authentication middleware
app.add_middleware(AuthMiddleware)

# Register routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
from src.routes.todos import router as todos_router
app.include_router(todos_router, prefix="/api/tasks", tags=["Todos"])


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    create_db_and_tables()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Todo API is running",
        "version": "1.0.0",
        "phase": "II",
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB health check
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


# TODO: Register routers here as they are created
# from src.routes.auth import router as auth_router
# from src.routes.todos import router as todos_router
# app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
# app.include_router(todos_router, prefix="/api/tasks", tags=["Todos"])
