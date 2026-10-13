"""Constraint satisfaction for portfolio feasibility."""

from app.ai.types import ConstraintBounds, FinancialContext, PortfolioAllocation, RiskProfile
from app.utils.financial_math import months_until


def derive_constraint_bounds(
    ctx: FinancialContext,
    risk: RiskProfile,
    monthly_capacity: float,
) -> ConstraintBounds:
    config = ctx.constraint_config
    max_by_profile = config.get(
        "max_equity_by_profile",
        {"conservative": 0.30, "moderate": 0.60, "aggressive": 0.80},
    )
    max_equity = float(max_by_profile.get(risk.dominant, 0.60))
    max_gold = float(config.get("max_gold", 0.15))
    min_cash = float(config.get("min_cash", 0.05))

    min_horizon = 999.0
    for goal in ctx.goals:
        months = months_until(goal.get("target_date"))
        years = months / 12.0
        if years < min_horizon:
            min_horizon = years
    if min_horizon == 999.0:
        min_horizon = 5.0

    if min_horizon < 3:
        max_equity = min(max_equity, 0.35)
        min_cash = max(min_cash, 0.15)

    explanations = [
        f"Maximum equity capped at {max_equity * 100:.0f}% for {risk.dominant} profile.",
        f"Gold allocation capped at {max_gold * 100:.0f}%.",
        f"Minimum cash/liquid allocation set to {min_cash * 100:.0f}%.",
    ]

    return ConstraintBounds(
        min_alloc={"equity": 0.0, "bonds": 0.0, "gold": 0.0, "cash": min_cash},
        max_alloc={"equity": max_equity, "bonds": 1.0, "gold": max_gold, "cash": 0.40},
        max_monthly_investment=max(monthly_capacity, 0),
        min_horizon_years=min_horizon,
        explanations=explanations,
    )


def is_feasible(allocation: PortfolioAllocation, bounds: ConstraintBounds, tolerance: float = 0.02) -> bool:
    values = allocation.as_dict()
    total = sum(values.values())
    if abs(total - 1.0) > tolerance:
        return False
    for key, value in values.items():
        if value < bounds.min_alloc.get(key, 0) - tolerance:
            return False
        if value > bounds.max_alloc.get(key, 1) + tolerance:
            return False
    return True


def constraint_violation_penalty(allocation: PortfolioAllocation, bounds: ConstraintBounds) -> float:
    penalty = 0.0
    values = allocation.as_dict()
    total = sum(values.values())
    penalty += abs(total - 1.0) * 10
    for key, value in values.items():
        if value < bounds.min_alloc.get(key, 0):
            penalty += (bounds.min_alloc[key] - value) * 5
        if value > bounds.max_alloc.get(key, 1):
            penalty += (value - bounds.max_alloc[key]) * 5
    return penalty
