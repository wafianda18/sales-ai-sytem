"""Auth endpoints."""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from config import DUMMY_USERS, ACCESS_TOKEN_EXPIRE_MINUTES
from middleware.auth import create_access_token
from models.schemas import LoginRequest, TokenResponse, UserInfo

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login & get JWT",
    responses={
        401: {"description": "Invalid credentials"},
    },
)
def login(body: LoginRequest):
    """
    Authenticate with username/password and receive a JWT Bearer token.

    **Demo credentials:**
    - `admin` / `admin123`
    - `analyst` / `analyst123`
    """
    user = DUMMY_USERS.get(body.username)
    if not user or user["password"] != body.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return TokenResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserInfo(
            username=user["username"],
            full_name=user["full_name"],
            role=user["role"],
        ),
    )
