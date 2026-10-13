"""Portfolio, simulation, warning, report schemas."""

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class PortfolioResponse(BaseModel):
    current_allocation: dict[str, float]
    target_allocation: dict[str, float]
    drift: dict[str, float]
    needs_rebalancing: bool


class WhatIfRequest(BaseModel):
    name: str = Field(default="Custom Scenario", max_length=120)
    monthly_income: Optional[float] = Field(default=None, ge=0)
    monthly_investment_override: Optional[float] = Field(default=None, ge=0)
    expense_multiplier: Optional[float] = Field(default=None, ge=0.1, le=3.0)
    goal_amount_override: Optional[float] = Field(default=None, gt=0)
    goal_date_override: Optional[datetime] = None
    risk_override: Optional[Literal["conservative", "moderate", "aggressive"]] = None


class WhatIfResponse(BaseModel):
    id: str
    name: str
    baseline: dict
    scenario: dict
    comparison: dict


class WarningResponse(BaseModel):
    code: str
    severity: Literal["critical", "high", "medium", "low", "informational"]
    message: str


class RebalancingResponse(BaseModel):
    target_allocation: dict[str, float]
    current_allocation: dict[str, float]
    drift: dict[str, float]
    suggestions: list[str]
    explanation: list[str]


class MonthlyReportSummary(BaseModel):
    id: str
    report_month: str
    generated_at: datetime
    health_score: int


class MonthlyReportResponse(BaseModel):
    id: str
    report_month: str
    financial_summary: dict
    investment_summary: dict
    goal_progress: list[dict]
    health_score: dict
    ai_analysis: list[str]
    warnings: list[dict]
    next_month_plan: dict
    generated_at: datetime
