"""Shared AI data structures."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FinancialContext:
    user_id: str
    profile: dict
    debts: list[dict]
    assets: list[dict]
    goals: list[dict]
    risk_assessment: dict | None
    constraint_config: dict
    asset_classes: list[dict]
    rules: list[dict]
    return_assumptions: dict[str, float] = field(default_factory=dict)


@dataclass
class ExpertConclusion:
    rule_id: str
    message: str
    priority: str
    weight: int = 0


@dataclass
class ExpertSystemResult:
    financial_status: str
    priorities: list[str]
    conclusions: list[ExpertConclusion]
    warnings: list[str] = field(default_factory=list)


@dataclass
class RiskProfile:
    conservative: float
    moderate: float
    aggressive: float
    dominant: str
    explanation: list[str]


@dataclass
class ConstraintBounds:
    min_alloc: dict[str, float]
    max_alloc: dict[str, float]
    max_monthly_investment: float
    min_horizon_years: float
    explanations: list[str] = field(default_factory=list)


@dataclass
class PortfolioAllocation:
    equity: float
    bonds: float
    gold: float
    cash: float

    def as_dict(self) -> dict[str, float]:
        return {
            "equity": self.equity,
            "bonds": self.bonds,
            "gold": self.gold,
            "cash": self.cash,
        }

    def as_list(self) -> list[float]:
        return [self.equity, self.bonds, self.gold, self.cash]

    @classmethod
    def from_list(cls, values: list[float]) -> "PortfolioAllocation":
        return cls(
            equity=values[0],
            bonds=values[1],
            gold=values[2],
            cash=values[3],
        )


@dataclass
class AIExecutionTrace:
    expert: ExpertSystemResult | None = None
    health: dict | None = None
    emergency_fund: dict | None = None
    capacity: dict | None = None
    risk: RiskProfile | None = None
    constraints: ConstraintBounds | None = None
    utility_scores: list[dict] = field(default_factory=list)
    ga_stats: dict = field(default_factory=dict)
    explanations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
