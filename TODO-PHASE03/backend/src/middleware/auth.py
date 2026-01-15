"""
Authentication middleware for extracting and verifying JWT from requests.
Attaches user_id to request state for use in dependency injection.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
from uuid import UUID
from src.auth.jwt import verify_and_extract_user_id, JWTVerificationError


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that extracts JWT from Authorization header or auth_token cookie.
    Verifies JWT and attaches user_id to request.state for protected routes.
    """

    # Routes that don't require authentication
    PUBLIC_PATHS = {
        "/",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/auth/signup",
        "/auth/signin",
    }

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process request and attach user_id if JWT is valid.
        """
        # Skip authentication for public paths
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        # Skip authentication for OPTIONS requests (CORS preflight)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Extract JWT token from Authorization header or cookie
        token = self._extract_token(request)

        if not token:
            # If route requires authentication, return 401
            if self._requires_auth(request.url.path):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "error": {
                            "code": "UNAUTHORIZED",
                            "message": "Authentication required",
                        }
                    },
                )
            return await call_next(request)

        # Verify JWT and extract user_id
        try:
            user_id = await verify_and_extract_user_id(token)
            request.state.user_id = user_id
        except JWTVerificationError as e:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": {"code": "UNAUTHORIZED", "message": "Invalid or expired token"}
                },
            )

        return await call_next(request)

    def _extract_token(self, request: Request) -> str:
        """
        Extract JWT token from Authorization header or auth_token cookie.

        Priority:
        1. Authorization header: "Bearer <token>"
        2. auth_token cookie
        """
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix

        # Check auth_token cookie
        auth_cookie = request.cookies.get("auth_token")
        if auth_cookie:
            return auth_cookie

        return None

    def _requires_auth(self, path: str) -> bool:
        """
        Determine if a path requires authentication.
        All /api/* routes require authentication.
        """
        return path.startswith("/api/")
