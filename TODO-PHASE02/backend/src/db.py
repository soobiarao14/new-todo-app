"""
Database engine configuration for Neon PostgreSQL with connection pooling.
"""
import os
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling
# pool_size: Maximum number of connections to maintain in the pool
# max_overflow: Maximum number of connections that can be created beyond pool_size
# pool_recycle: Recycle connections after 3600 seconds (1 hour) to prevent stale connections
# pool_pre_ping: Enable connection health checks before using a connection
# connect_args: Additional connection arguments (SSL required for Neon)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging in development
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True,
    # SSL is already in the URL, no need for connect_args
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.
    This should be called once during application startup.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency function to get a database session.
    Usage in FastAPI endpoints:
        def my_endpoint(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
