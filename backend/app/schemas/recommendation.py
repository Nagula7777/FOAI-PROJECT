"""Recommendation and AI analysis schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AllocationResponse(BaseModel):
    equity: float
    bonds: float
    gold: float
    cash: float


class RecommendationResponse(BaseModel):
    id: str
    generated_at: datetime
    monthly_investment_amount: float
    recommended_horizon_years: float
    allocation: AllocationResponse
    recommended_products: list[dict]
    risk_profile: dict
    investment_capacity_breakdown: dict
    explanations: list[str]
    disclaimer: str


class FinancialHealthResponse(BaseModel):
    total_score: int
    components: dict[str, dict]
    explanation: list[str]


class EmergencyFundResponse(BaseModel):
    required_amount: float
    current_amount: float
    remaining_amount: float
    recommended_monthly_contribution: float
    explanation: list[str]


class InvestmentCapacityResponse(BaseModel):
    monthly_income: float
    essential_expenses: float
    debt_obligations: float
    emergency_contribution: float
    available_investment: float
    breakdown: list[str]


class AnalyzeResponse(BaseModel):
    health: FinancialHealthResponse
    emergency_fund: EmergencyFundResponse
    capacity: InvestmentCapacityResponse
    risk_profile: dict
    recommendation: RecommendationResponse
    warnings: list[dict]
    trace_summary: dict[str, Any]
