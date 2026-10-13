"""Profile, debt, and asset routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.profile import (
    AssetCreateRequest,
    AssetResponse,
    DebtCreateRequest,
    DebtResponse,
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.services import profile_service

router = APIRouter(tags=["Profile"])


@router.get("/api/profile", response_model=ProfileResponse | None)
async def get_profile(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await profile_service.get_profile(current_user.id)


@router.put("/api/profile", response_model=ProfileResponse)
async def update_profile(
    payload: ProfileUpdateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await profile_service.upsert_profile(current_user.id, payload)


@router.get("/api/debts", response_model=list[DebtResponse])
async def list_debts(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await profile_service.list_debts(current_user.id)


@router.post("/api/debts", response_model=DebtResponse)
async def create_debt(
    payload: DebtCreateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await profile_service.create_debt(current_user.id, payload)


@router.put("/api/debts/{debt_id}", response_model=DebtResponse)
async def update_debt(
    debt_id: str,
    payload: DebtCreateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await profile_service.update_debt(current_user.id, debt_id, payload)


@router.delete("/api/debts/{debt_id}")
async def delete_debt(
    debt_id: str,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    await profile_service.delete_debt(current_user.id, debt_id)
    return {"message": "Debt deleted"}


@router.get("/api/assets", response_model=list[AssetResponse])
async def list_assets(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await profile_service.list_assets(current_user.id)


@router.post("/api/assets", response_model=AssetResponse)
async def create_asset(
    payload: AssetCreateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await profile_service.create_asset(current_user.id, payload)


@router.put("/api/assets/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: str,
    payload: AssetCreateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await profile_service.update_asset(current_user.id, asset_id, payload)


@router.delete("/api/assets/{asset_id}")
async def delete_asset(
    asset_id: str,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    await profile_service.delete_asset(current_user.id, asset_id)
    return {"message": "Asset deleted"}
