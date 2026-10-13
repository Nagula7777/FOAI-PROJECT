"""Utility-based portfolio scoring."""

from app.ai.types import ConstraintBounds, FinancialContext, PortfolioAllocation, RiskProfile
from app.ai.constraints import constraint_violation_penalty


DEFAULT_RETURNS = {"equity": 0.11, "bonds": 0.07, "gold": 0.08, "cash": 0.04}
DEFAULT_RISK = {"equity": 0.75, "bonds": 0.35, "gold": 0.45, "cash": 0.10}


def calculate_utility(
    allocation: PortfolioAllocation,
    ctx: FinancialContext,
    risk: RiskProfile,
    bounds: ConstraintBounds,
    priorities: list[str],
) -> float:
    returns = ctx.return_assumptions or DEFAULT_RETURNS
    values = allocation.as_dict()

    expected_return = sum(values[k] * returns.get(k, 0.05) for k in values)
    portfolio_risk = sum(values[k] * DEFAULT_RISK.get(k, 0.3) for k in values)

    risk_target = {"conservative": 0.25, "moderate": 0.45, "aggressive": 0.65}[risk.dominant]
    risk_fit = 1 - abs(portfolio_risk - risk_target)

    diversification = 1 - max(values.values())

    liquidity = values.get("cash", 0) + values.get("bonds", 0) * 0.5
    liquidity_score = min(liquidity / 0.35, 1.0)

    goal_fit = 0.7
    if "capital_preservation" in priorities:
        goal_fit = values.get("cash", 0) + values.get("bonds", 0)
    elif "investment_growth" in priorities:
        goal_fit = values.get("equity", 0) + values.get("gold", 0) * 0.3

    penalty = constraint_violation_penalty(allocation, bounds)

    utility = (
        0.30 * expected_return
        + 0.20 * risk_fit
        + 0.15 * goal_fit
        + 0.15 * liquidity_score
        + 0.10 * diversification
        + 0.10 * (1 - penalty)
    )
    return max(utility - penalty, 0.0)
