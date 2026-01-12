"""
Better Auth configuration module.
Loads authentication settings from environment variables.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BetterAuthConfig:
    """Configuration for Better Auth integration."""

    def __init__(self):
        self.secret: str = self._get_required_env("BETTER_AUTH_SECRET")
        self.jwks_url: str = self._get_required_env("BETTER_AUTH_JWKS_URL")
        self.base_url: str = self._get_required_env("BETTER_AUTH_BASE_URL")

    @staticmethod
    def _get_required_env(key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Required environment variable {key} is not set")
        return value

    @staticmethod
    def get_optional_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """Get optional environment variable with default."""
        return os.getenv(key, default)


# Global configuration instance
auth_config = BetterAuthConfig()
