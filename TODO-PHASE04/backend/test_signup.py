"""Test the complete signup flow"""
from src.db import engine, create_db_and_tables
from src.models.user import User
from src.routes.auth import hash_password
from sqlmodel import Session, select
from uuid import uuid4
from datetime import datetime

print("Creating tables...")
create_db_and_tables()

test_email = "testsignup@example.com"
test_password = "password123"

print(f"Testing signup for {test_email}...")

try:
    # Hash password
    password_hash = hash_password(test_password)
    print(f"[OK] Password hashed: {password_hash[:20]}...")

    # Create session
    with Session(engine) as session:
        # Check if user exists
        existing_user = session.exec(select(User).where(User.email == test_email)).first()

        if existing_user:
            print(f"[INFO] User already exists, deleting...")
            session.delete(existing_user)
            session.commit()

        # Create new user
        new_user = User(
            id=uuid4(),
            email=test_email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        print(f"[INFO] Creating user object...")
        session.add(new_user)

        print(f"[INFO] Committing to database...")
        session.commit()

        print(f"[INFO] Refreshing user object...")
        session.refresh(new_user)

        print(f"[OK] User created successfully!")
        print(f"  ID: {new_user.id}")
        print(f"  Email: {new_user.email}")
        print(f"  Created: {new_user.created_at}")

except Exception as e:
    print(f"[ERROR] Failed to create user: {e}")
    import traceback
    traceback.print_exc()
