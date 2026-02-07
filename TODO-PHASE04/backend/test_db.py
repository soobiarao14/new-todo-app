from src.db import engine, create_db_and_tables
from sqlmodel import text

print("Testing database connection...")

# Create tables
try:
    create_db_and_tables()
    print("[OK] Tables created/verified")
except Exception as e:
    print(f"[ERROR] Error creating tables: {e}")

# Check tables
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
        tables = [row[0] for row in result]
        print(f"[OK] Tables in database: {tables}")
except Exception as e:
    print(f"[ERROR] Error checking tables: {e}")

# Test signup logic
print("\nTesting signup logic...")
try:
    from src.models.user import User
    from src.routes.auth import hash_password
    from sqlmodel import Session, select

    test_email = "test@example.com"
    test_password = "testpass123"

    # Hash password
    password_hash = hash_password(test_password)
    print(f"[OK] Password hashed successfully")

    # Check if user exists
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == test_email)).first()
        if existing_user:
            print(f"[OK] Test user already exists: {existing_user.email}")
        else:
            print(f"[OK] Test user does not exist yet")

except Exception as e:
    print(f"[ERROR] Error in signup logic: {e}")
    import traceback
    traceback.print_exc()
