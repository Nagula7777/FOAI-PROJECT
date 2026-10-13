"""Risk assessment schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RiskAssessmentRequest(BaseModel):
    loss_tolerance: int = Field(ge=1, le=5)
    market_reaction: int = Field(ge=1, le=5)
    investment_knowledge: int = Field(ge=1, le=5)
    horizon_comfort: int = Field(ge=1, le=5)
    volatility_comfort: int = Field(ge=1, le=5)


class FuzzyMembership(BaseModel):
    conservative: float
    moderate: float
    aggressive: float


class RiskAssessmentResponse(BaseModel):
    id: str
    questionnaire_score: int
    fuzzy_output: FuzzyMembership
    dominant_profile: Literal["conservative", "moderate", "aggressive"]
    explanation: list[str]
    assessed_at: datetime
