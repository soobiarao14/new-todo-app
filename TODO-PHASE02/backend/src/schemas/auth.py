"""
Authentication request/response schemas for signup, signin, and session management.
"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class SignupRequest(BaseModel):
    """Request schema for user signup."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")


class SigninRequest(BaseModel):
    """Request schema for user signin."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """User information returned in auth responses."""

    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email address")

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility


class AuthResponse(BaseModel):
    """Response schema for successful authentication (signup/signin)."""

    user: UserResponse = Field(..., description="User information")
    token: str = Field(..., description="JWT access token")


class SignoutResponse(BaseModel):
    """Response schema for signout."""

    message: str = Field(default="Signed out successfully")


class SessionResponse(BaseModel):
    """Response schema for session validation."""

    user: UserResponse = Field(..., description="Current user information")
    authenticated: bool = Field(default=True, description="Authentication status")
