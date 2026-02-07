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
# Import models to ensure tables are registered with SQLModel before create_db_and_tables()
from src.models import User, Todo, Conversation, Message

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
    "http://127.0.0.1:3000",
    "http://192.168.2.107:3000",
    "https://new-todo-app-kappa.vercel.app",
]

# IMPORTANT: Middleware is executed in REVERSE order of addition.
# Add inner middlewares first, CORS middleware last (so it runs first/outermost).

# Add security headers middleware (runs third - innermost)
app.add_middleware(SecurityHeadersMiddleware)

# Add authentication middleware (runs second)
app.add_middleware(AuthMiddleware)

# Add CORS middleware LAST so it runs FIRST (outermost layer)
# This ensures CORS headers are set before any other middleware can reject the request
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["*"],
    allow_headers=["*"],
)




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


# Register routers
from src.routes.auth import router as auth_router
from src.routes.todos import router as todos_router
from src.routes.chat import router as chat_router
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(todos_router, prefix="/api/tasks", tags=["Todos"])
# Phase III: AI Chatbot routes
app.include_router(chat_router, prefix="/api", tags=["Chat"])


# chnagecode...............main ne kiya h





