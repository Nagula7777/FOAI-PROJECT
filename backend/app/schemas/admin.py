"""Admin Pydantic schemas."""

from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    asset_class: Literal["equity", "bonds", "gold", "cash"]
    risk_category: Literal["moderate", "high", "low"] = "moderate"
    expected_return_assumption: float = Field(ge=0, le=1)
    liquidity: Literal["high", "medium", "low"] = "medium"
    min_horizon_years: float = Field(ge=0)
    is_active: bool = True


class RuleCreateRequest(BaseModel):
    rule_id: str = Field(min_length=1, max_length=80)
    category: str = "priority"
    condition: str = ""
    action: str = ""
    priority_weight: int = Field(ge=0, le=100)
    message_template: str = ""
    is_active: bool = True


class ConstraintUpdateRequest(BaseModel):
    max_equity_by_profile: dict[str, float]
    max_gold: float = Field(ge=0, le=1)
    min_cash: float = Field(ge=0, le=1)
    allocation_sum_tolerance: float = 0.01


class UserAdminResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    onboarding_completed: bool
    created_at: datetime


class ActivityLogResponse(BaseModel):
    id: str
    actor_id: str
    action: str
    entity: str
    details: dict[str, Any]
    timestamp: datetime
