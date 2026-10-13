"""Authentication API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.services.auth_service import login_user, register_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegisterRequest) -> TokenResponse:
    return await register_user(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest) -> TokenResponse:
    return await login_user(payload)


@router.get("/me", response_model=UserResponse)
async def me(current_user: Annotated[UserResponse, Depends(get_current_user)]) -> UserResponse:
    return current_user
