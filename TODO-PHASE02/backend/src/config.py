"""
Environment configuration module.
Loads the appropriate .env file based on the APP_ENV environment variable.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


def load_environment():
    """
    Load environment variables from the appropriate .env file.

    Priority:
    1. If APP_ENV is set to 'production', load .env.production
    2. If APP_ENV is set to 'local' or not set, load .env.local
    3. Fallback to .env if specific files don't exist

    Usage:
        - For local development: No action needed (defaults to .env.local)
        - For production: Set APP_ENV=production before running
    """
    # Get the backend directory (parent of src)
    backend_dir = Path(__file__).parent.parent

    # Determine which environment to load
    app_env = os.getenv("APP_ENV", "local")

    # Define environment file paths
    env_files = {
        "production": backend_dir / ".env.production",
        "local": backend_dir / ".env.local",
        "default": backend_dir / ".env"
    }

    # Load the appropriate environment file
    # Use override=True to ensure the file values take precedence
    if app_env == "production" and env_files["production"].exists():
        load_dotenv(env_files["production"], override=True)
        print(f"[OK] Loaded production environment from {env_files['production']}")
    elif env_files["local"].exists():
        load_dotenv(env_files["local"], override=True)
        print(f"[OK] Loaded local environment from {env_files['local']}")
    elif env_files["default"].exists():
        load_dotenv(env_files["default"], override=True)
        print(f"[OK] Loaded default environment from {env_files['default']}")
    else:
        print("[WARNING] No environment file found. Using system environment variables only.")

    # Validate required environment variables
    required_vars = [
        "DATABASE_URL",
        "BETTER_AUTH_SECRET",
        "BETTER_AUTH_JWKS_URL",
        "BETTER_AUTH_BASE_URL"
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please ensure your .env file contains all required variables."
        )

    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_url": os.getenv("DATABASE_URL"),
        "allowed_origins": os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
        "auth_base_url": os.getenv("BETTER_AUTH_BASE_URL"),
    }


# Load environment on module import
config = load_environment()
