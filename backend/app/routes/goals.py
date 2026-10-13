"""Goal routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.goal import GoalAnalysisResponse, GoalCreateRequest, GoalResponse, GoalUpdateRequest
from app.services import goal_service

router = APIRouter(prefix="/api/goals", tags=["Goals"])


@router.get("", response_model=list[GoalResponse])
async def list_goals(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await goal_service.list_goals(current_user.id)


@router.post("", response_model=GoalResponse)
async def create_goal(
    payload: GoalCreateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await goal_service.create_goal(current_user.id, payload)


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(goal_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await goal_service.get_goal(current_user.id, goal_id)


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: str,
    payload: GoalUpdateRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await goal_service.update_goal(current_user.id, goal_id, payload)


@router.delete("/{goal_id}")
async def delete_goal(goal_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    await goal_service.delete_goal(current_user.id, goal_id)
    return {"message": "Goal deleted"}


@router.get("/{goal_id}/analysis", response_model=GoalAnalysisResponse)
async def goal_analysis(goal_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await goal_service.analyze_goal_by_id(current_user.id, goal_id)
