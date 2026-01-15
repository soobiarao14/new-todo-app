"""
FastAPI dependency functions for authentication and authorization.
"""
from fastapi import Request, HTTPException, status
from uuid import UUID


def get_current_user_id(request: Request) -> UUID:
    """
    Dependency function to get authenticated user_id from request state.

    The AuthMiddleware attaches user_id to request.state after verifying JWT.
    This dependency retrieves that user_id or raises 401 if not present.

    Usage in route handlers:
        @router.get("/api/tasks")
        async def list_tasks(user_id: UUID = Depends(get_current_user_id)):
            # user_id is guaranteed to be from verified JWT
            ...

    Returns:
        UUID: Authenticated user's ID

    Raises:
        HTTPException: 401 Unauthorized if user_id not in request state
    """
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": {"code": "UNAUTHORIZED", "message": "Authentication required"}
            },
        )

    return user_id
