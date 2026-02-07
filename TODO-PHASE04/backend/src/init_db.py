"""
Database initialization script.
Run this once to create all database tables.
"""
from src.db import create_db_and_tables
from src.models.user import User
from src.models.todo import Todo


def init_database():
    """
    Initialize database by creating all tables.
    Tables created:
    - users (managed by Better Auth)
    - todos (application-managed with user_id FK)
    """
    print("Initializing database...")
    print("Creating tables: users, todos")

    try:
        create_db_and_tables()
        print("✓ Database tables created successfully")
        print("  - users table ready (Better Auth managed)")
        print("  - todos table ready (user_id foreign key to users)")
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    init_database()
