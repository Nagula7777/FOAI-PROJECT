"""Financial profile schemas."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    age: int = Field(ge=18, le=100)
    employment_status: Literal["employed", "self_employed", "unemployed", "retired"]
    dependents: int = Field(ge=0, le=20)


class IncomeInfo(BaseModel):
    monthly_income: float = Field(ge=0)
    other_monthly_income: float = Field(ge=0, default=0)


class ExpenseInfo(BaseModel):
    rent: float = Field(ge=0, default=0)
    food: float = Field(ge=0, default=0)
    transportation: float = Field(ge=0, default=0)
    education: float = Field(ge=0, default=0)
    utilities: float = Field(ge=0, default=0)
    healthcare: float = Field(ge=0, default=0)
    other: float = Field(ge=0, default=0)


class ProfileUpdateRequest(BaseModel):
    personal: PersonalInfo
    income: IncomeInfo
    expenses: ExpenseInfo
    income_stability: Literal["low", "medium", "high"] = "medium"
    investment_experience: Literal["none", "beginner", "intermediate", "advanced"] = "beginner"


class ProfileResponse(BaseModel):
    id: str
    user_id: str
    personal: PersonalInfo
    income: IncomeInfo
    expenses: ExpenseInfo
    income_stability: str
    investment_experience: str
    created_at: datetime
    updated_at: datetime


class DebtCreateRequest(BaseModel):
    loan_type: Literal["home", "personal", "education", "credit_card", "other"]
    outstanding_amount: float = Field(ge=0)
    emi: float = Field(ge=0)
    interest_rate: float = Field(ge=0, le=100)


class DebtResponse(BaseModel):
    id: str
    user_id: str
    loan_type: str
    outstanding_amount: float
    emi: float
    interest_rate: float
    is_high_interest: bool


class AssetCreateRequest(BaseModel):
    asset_class: Literal["cash", "equity", "bonds", "gold", "other"]
    name: str = Field(min_length=1, max_length=120)
    current_value: float = Field(ge=0)
    is_emergency_fund: bool = False


class AssetResponse(BaseModel):
    id: str
    user_id: str
    asset_class: str
    name: str
    current_value: float
    is_emergency_fund: bool
