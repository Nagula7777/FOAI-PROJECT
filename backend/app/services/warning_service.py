"""Rule-based financial warnings."""

from app.ai.types import FinancialContext
from app.utils.financial_math import asset_total_by_class, safe_divide, total_expenses, total_income


def detect_warnings(ctx: FinancialContext, analysis: dict) -> list[dict]:
    warnings: list[dict] = []
    income = total_income(ctx.profile.get("income", {}))
    expenses = total_expenses(ctx.profile.get("expenses", {}))

    emergency = analysis.get("emergency_fund", {})
    if emergency.get("remaining_amount", 0) > 0:
        warnings.append(
            {
                "code": "EMERGENCY_FUND_INSUFFICIENT",
                "severity": "high",
                "message": f"Emergency fund shortfall of {emergency['remaining_amount']:.0f}.",
            }
        )

    if safe_divide(expenses, income, 1) > 0.7:
        warnings.append(
            {
                "code": "EXPENSES_TOO_HIGH",
                "severity": "medium",
                "message": "Essential expenses exceed 70% of income.",
            }
        )

    capacity = analysis.get("capacity", {})
    if capacity.get("available_investment", 0) < income * 0.05:
        warnings.append(
            {
                "code": "LOW_INVESTMENT_CAPACITY",
                "severity": "medium",
                "message": "Available investment capacity is low after obligations.",
            }
        )

    for goal in ctx.goals:
        if goal.get("status") == "unlikely":
            warnings.append(
                {
                    "code": "GOAL_BEHIND",
                    "severity": "high",
                    "message": f"Goal '{goal.get('name')}' is unlikely to be met on current plan.",
                }
            )

    totals = asset_total_by_class(ctx.assets)
    total_value = sum(totals.values()) or 1
    for cls, value in totals.items():
        if value / total_value > 0.7:
            warnings.append(
                {
                    "code": "EXCESSIVE_CONCENTRATION",
                    "severity": "medium",
                    "message": f"Portfolio is concentrated in {cls} ({value / total_value:.0%}).",
                }
            )

    allocation = analysis.get("recommendation", {}).get("allocation", {})
    short_horizon = any(
        ctx.goals and True for _ in [1]
    )
    if short_horizon and allocation.get("equity", 0) > 0.5:
        warnings.append(
            {
                "code": "SHORT_TERM_HIGH_RISK",
                "severity": "high",
                "message": "Short-term goals present but equity allocation is relatively high.",
            }
        )

    return warnings
