"""Health and onboarding status routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.config.constants import FINANCIAL_DISCLAIMER
from app.dependencies.auth import get_current_user
from app.schemas.auth import UserResponse

router = APIRouter(tags=["System"])


@router.get("/api/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "foai-financial-planner"}


@router.get("/api/onboarding/status")
async def onboarding_status(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> dict:
    return {
        "onboarding_completed": current_user.onboarding_completed,
        "disclaimer": FINANCIAL_DISCLAIMER,
    }
