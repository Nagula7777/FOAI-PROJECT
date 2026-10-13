"""Risk, health, and AI routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.ai.health_scorer import calculate_health_score
from app.ai.recommendation_engine import _emergency_fund_analysis, _investment_capacity
from app.ai.expert_system import evaluate_expert_system
from app.dependencies.auth import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.recommendation import AnalyzeResponse
from app.schemas.risk import RiskAssessmentRequest, RiskAssessmentResponse
from app.services import ai_service, risk_service
from app.services.context_builder import build_financial_context

router = APIRouter(tags=["AI & Health"])


@router.post("/api/risk-assessment", response_model=RiskAssessmentResponse)
async def submit_risk(
    payload: RiskAssessmentRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await risk_service.submit_risk_assessment(current_user.id, payload)


@router.get("/api/risk-assessment/latest", response_model=RiskAssessmentResponse | None)
async def latest_risk(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await risk_service.get_latest_risk_assessment(current_user.id)


@router.get("/api/financial-health")
async def financial_health(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    ctx = await build_financial_context(current_user.id)
    return calculate_health_score(ctx)


@router.get("/api/emergency-fund")
async def emergency_fund(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    ctx = await build_financial_context(current_user.id)
    return _emergency_fund_analysis(ctx)


@router.get("/api/investment-capacity")
async def investment_capacity(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    ctx = await build_financial_context(current_user.id)
    expert = evaluate_expert_system(ctx)
    emergency = _emergency_fund_analysis(ctx)
    return _investment_capacity(ctx, emergency, expert.priorities)


@router.post("/api/ai/analyze")
async def analyze(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await ai_service.run_full_analysis(current_user.id)


@router.get("/api/ai/recommendation")
async def get_recommendation(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    rec = await ai_service.get_latest_recommendation(current_user.id)
    if not rec:
        raise HTTPException(status_code=404, detail="No recommendation found. Run AI analysis first.")
    return rec
