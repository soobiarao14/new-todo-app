"""
Authentication router with signup, signin, signout, and session endpoints.

NOTE: This is a simplified implementation for Phase II.
In production, this would proxy to Better Auth for user management.
For this implementation, we're using basic password hashing with bcrypt.
"""
from fastapi import APIRouter, HTTPException, Response, Depends, status
from sqlmodel import Session, select
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from uuid import uuid4
from src.schemas.auth import (
    SignupRequest,
    SigninRequest,
    AuthResponse,
    SignoutResponse,
    SessionResponse,
    UserResponse,
)
from src.models.user import User
from src.db import get_session
from src.dependencies import get_current_user_id
from src.auth.config import auth_config
from uuid import UUID
from fastapi import Request

router = APIRouter()

# Password hashing context (bcrypt with cost factor 12)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_jwt_token(user_id: UUID, email: str) -> str:
    """
    Create JWT token with user_id in 'sub' claim.
    Expires in 1 hour (3600 seconds).
    """
    payload = {
        "sub": str(user_id),  # User ID in 'sub' claim
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=1),  # 1 hour expiration
        "iat": datetime.utcnow(),  # Issued at
    }

    # Sign token with RS256 algorithm (would use Better Auth's key in production)
    # For Phase II, using HS256 with secret key as simplified implementation
    token = jwt.encode(payload, auth_config.secret, algorithm="HS256")
    return token


def set_auth_cookie(response: Response, token: str):
    """
    Set httpOnly cookie with JWT token.
    Cookie settings:
    - httponly: True (prevent XSS access)
    - secure: True in production (HTTPS only)
    - samesite: strict (prevent CSRF)
    - max_age: 3600 seconds (1 hour)
    """
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="strict",
        max_age=3600,  # 1 hour
    )


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    signup_data: SignupRequest, response: Response, session: Session = Depends(get_session)
):
    """
    User signup endpoint.

    1. Validates email and password
    2. Checks if email already exists
    3. Hashes password with bcrypt
    4. Creates user in database
    5. Generates JWT token
    6. Sets httpOnly cookie
    7. Returns user info and token
    """
    print(f"[SIGNUP] Starting signup for {signup_data.email}")

    try:
        # Check if email already exists
        print(f"[SIGNUP] Checking if user exists...")
        existing_user = session.exec(select(User).where(User.email == signup_data.email)).first()
        if existing_user:
            print(f"[SIGNUP] User already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "error": {"code": "EMAIL_EXISTS", "message": "Email already registered"}
                },
            )

        # Hash password
        print(f"[SIGNUP] Hashing password...")
        password_hash = hash_password(signup_data.password)
        print(f"[SIGNUP] Password hashed successfully")

        # Create user
        print(f"[SIGNUP] Creating user object...")
        new_user = User(
            id=uuid4(), email=signup_data.email, password_hash=password_hash, created_at=datetime.utcnow(), updated_at=datetime.utcnow()
        )

        print(f"[SIGNUP] Adding user to session...")
        session.add(new_user)

        print(f"[SIGNUP] Committing to database...")
        session.commit()

        print(f"[SIGNUP] Refreshing user object...")
        session.refresh(new_user)
        print(f"[SIGNUP] User created with ID: {new_user.id}")

        # Generate JWT token
        print(f"[SIGNUP] Generating JWT token...")
        token = create_jwt_token(new_user.id, new_user.email)
        print(f"[SIGNUP] Token generated")

        # Set httpOnly cookie
        print(f"[SIGNUP] Setting auth cookie...")
        set_auth_cookie(response, token)
        print(f"[SIGNUP] Cookie set")

        print(f"[SIGNUP] Creating response...")
        auth_response = AuthResponse(user=UserResponse(id=new_user.id, email=new_user.email), token=token)
        print(f"[SIGNUP] Response created, returning...")
        return auth_response
    except HTTPException:
        raise
    except Exception as e:
        print(f"[SIGNUP] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise


@router.post("/signin", response_model=AuthResponse)
async def signin(
    signin_data: SigninRequest, response: Response, session: Session = Depends(get_session)
):
    """
    User signin endpoint.

    1. Validates credentials
    2. Checks if user exists
    3. Verifies password
    4. Generates JWT token
    5. Sets httpOnly cookie
    6. Returns user info and token
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == signin_data.email)).first()

    if not user or not verify_password(signin_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "Invalid email or password",
                }
            },
        )

    # Generate JWT token
    token = create_jwt_token(user.id, user.email)

    # Set httpOnly cookie
    set_auth_cookie(response, token)

    return AuthResponse(user=UserResponse(id=user.id, email=user.email), token=token)


@router.post("/signout", response_model=SignoutResponse)
async def signout(response: Response):
    """
    User signout endpoint.
    Clears the auth_token cookie.
    """
    response.delete_cookie(key="auth_token")
    return SignoutResponse(message="Signed out successfully")


@router.get("/session", response_model=SessionResponse)
async def get_session_info(
    user_id: UUID = Depends(get_current_user_id), session: Session = Depends(get_session)
):
    """
    Get current session information.
    Returns user info if authenticated.
    """
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": {"code": "USER_NOT_FOUND", "message": "User not found"}},
        )

    return SessionResponse(
        user=UserResponse(id=user.id, email=user.email), authenticated=True
    )
