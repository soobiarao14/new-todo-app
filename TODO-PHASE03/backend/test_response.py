"""Test the UserResponse and AuthResponse schemas"""
from src.schemas.auth import UserResponse, AuthResponse
from uuid import uuid4

print("Testing UserResponse schema...")

try:
    test_id = uuid4()
    test_email = "test@example.com"

    user_response = UserResponse(id=test_id, email=test_email)
    print(f"[OK] UserResponse created: {user_response}")
    print(f"  ID type: {type(user_response.id)}")
    print(f"  Email: {user_response.email}")

    # Test AuthResponse
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    auth_response = AuthResponse(user=user_response, token=test_token)
    print(f"[OK] AuthResponse created: {auth_response}")

    # Test serialization
    json_data = auth_response.model_dump()
    print(f"[OK] Serialized to dict: {json_data}")

    json_str = auth_response.model_dump_json()
    print(f"[OK] Serialized to JSON: {json_str[:100]}...")

except Exception as e:
    print(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()
