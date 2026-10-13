"""Financial goal schemas."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class GoalCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: Literal[
        "emergency_fund",
        "education",
        "vehicle",
        "house",
        "marriage",
        "retirement",
        "travel",
        "other",
    ]
    target_amount: float = Field(gt=0)
    current_amount: float = Field(ge=0, default=0)
    target_date: datetime
    priority: int = Field(ge=1, le=10, default=5)
    monthly_contribution: float = Field(ge=0, default=0)


class GoalUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    category: Optional[
        Literal[
            "emergency_fund",
            "education",
            "vehicle",
            "house",
            "marriage",
            "retirement",
            "travel",
            "other",
        ]
    ] = None
    target_amount: Optional[float] = Field(default=None, gt=0)
    current_amount: Optional[float] = Field(default=None, ge=0)
    target_date: Optional[datetime] = None
    priority: Optional[int] = Field(default=None, ge=1, le=10)
    monthly_contribution: Optional[float] = Field(default=None, ge=0)


class GoalResponse(BaseModel):
    id: str
    user_id: str
    name: str
    category: str
    target_amount: float
    current_amount: float
    target_date: datetime
    priority: int
    monthly_contribution: float
    status: str


class GoalAnalysisResponse(BaseModel):
    goal_id: str
    current_amount: float
    target_amount: float
    remaining_amount: float
    months_remaining: float
    current_monthly_contribution: float
    required_monthly_contribution: float
    estimated_future_value: float
    status: Literal["on_track", "at_risk", "unlikely"]
    assumption_note: str
