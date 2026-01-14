"""
FastAPI application instance with CORS middleware and authentication.
Phase II Full-Stack Todo Application Backend.
"""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from src.config import config  # Load environment-specific configuration
from src.middleware.auth import AuthMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
from src.middleware.error_handler import (
    global_exception_handler,
    validation_exception_handler,
    http_exception_handler,
)
from src.routes.auth import router as auth_router
from src.db import create_db_and_tables

# Initialize FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II Full-Stack Todo Application - RESTful API with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://new-todo-app-kappa.vercel.app",
]

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

# Add security headers middleware
app.add_middleware(SecurityHeadersMiddleware)




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
from src.routes.auth import router as auth_router
from src.routes.todos import router as todos_router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(todos_router, prefix="/api/tasks", tags=["Todos"])
