"""
JWKS (JSON Web Key Set) fetcher for retrieving and caching public keys from Better Auth.
"""
import httpx
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from src.auth.config import auth_config


class JWKSFetcher:
    """
    Fetches and caches JWKS (public keys) from Better Auth.
    Caches keys for 1 hour to reduce external API calls.
    """

    def __init__(self):
        self._cache: Optional[Dict] = None
        self._cache_expires_at: Optional[datetime] = None
        self._cache_duration = timedelta(hours=1)

    async def get_jwks(self) -> Dict:
        """
        Fetch JWKS from Better Auth endpoint.
        Returns cached version if still valid.
        """
        # Check cache validity
        if self._cache and self._cache_expires_at:
            if datetime.utcnow() < self._cache_expires_at:
                return self._cache

        # Fetch fresh JWKS
        async with httpx.AsyncClient() as client:
            response = await client.get(
                auth_config.jwks_url, timeout=10.0, follow_redirects=True
            )
            response.raise_for_status()
            jwks_data = response.json()

            # Cache the result
            self._cache = jwks_data
            self._cache_expires_at = datetime.utcnow() + self._cache_duration

            return jwks_data

    async def get_signing_keys(self) -> List[Dict]:
        """
        Get list of signing keys from JWKS.
        Returns keys array from the JWKS response.
        """
        jwks = await self.get_jwks()
        return jwks.get("keys", [])

    def clear_cache(self):
        """Clear cached JWKS (useful for testing or forced refresh)."""
        self._cache = None
        self._cache_expires_at = None


# Global JWKS fetcher instance
jwks_fetcher = JWKSFetcher()
