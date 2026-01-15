"""
JWT verification using python-jose.
Verifies signature, expiration, and extracts user_id from 'sub' claim.
"""
from jose import jwt, jwk, JWTError
from jose.utils import base64url_decode
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID
from src.auth.jwks import jwks_fetcher
from src.auth.config import auth_config


class JWTVerificationError(Exception):
    """Custom exception for JWT verification failures."""

    pass


async def verify_jwt(token: str) -> Dict:
    """
    Verify JWT token signature and expiration.

    NOTE: Phase II simplified implementation uses HS256 (symmetric key).
    Production would use RS256 (asymmetric) with Better Auth JWKS.

    Args:
        token: JWT token string

    Returns:
        Decoded JWT payload with claims

    Raises:
        JWTVerificationError: If token is invalid, expired, or signature doesn't match
    """
    try:
        # Simplified implementation: Use HS256 with secret key
        # Production would fetch JWKS and use RS256
        payload = jwt.decode(
            token,
            auth_config.secret,
            algorithms=["HS256"],
            options={"verify_aud": False},
        )

        # Verify expiration manually (python-jose does this, but double-check)
        exp = payload.get("exp")
        if exp:
            exp_datetime = datetime.fromtimestamp(exp)
            if datetime.utcnow() > exp_datetime:
                raise JWTVerificationError("JWT token has expired")

        return payload

    except JWTError as e:
        raise JWTVerificationError(f"JWT verification failed: {str(e)}")
    except Exception as e:
        raise JWTVerificationError(f"Unexpected error during JWT verification: {str(e)}")


def extract_user_id(payload: Dict) -> UUID:
    """
    Extract user_id from JWT payload 'sub' claim.

    Args:
        payload: Decoded JWT payload

    Returns:
        User ID as UUID

    Raises:
        JWTVerificationError: If 'sub' claim is missing or invalid UUID
    """
    sub = payload.get("sub")
    if not sub:
        raise JWTVerificationError("JWT payload missing 'sub' claim (user ID)")

    try:
        return UUID(sub)
    except ValueError:
        raise JWTVerificationError(f"Invalid UUID format in 'sub' claim: {sub}")


async def verify_and_extract_user_id(token: str) -> UUID:
    """
    Convenience function: verify JWT and extract user_id in one call.

    Args:
        token: JWT token string

    Returns:
        User ID as UUID

    Raises:
        JWTVerificationError: If verification fails or user_id extraction fails
    """
    payload = await verify_jwt(token)
    return extract_user_id(payload)
