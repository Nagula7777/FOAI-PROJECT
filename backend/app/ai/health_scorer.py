"""Rule-based financial health scoring (0-100)."""

from app.ai.types import FinancialContext
from app.utils.financial_math import (
    current_emergency_fund,
    safe_divide,
    total_debt_outstanding,
    total_emi,
    total_expenses,
    total_income,
)


def _score_component(value: float, thresholds: list[tuple[float, int]]) -> int:
    for threshold, score in thresholds:
        if value >= threshold:
            return score
    return thresholds[-1][1]


def calculate_health_score(ctx: FinancialContext) -> dict:
    income = total_income(ctx.profile.get("income", {}))
    expenses = total_expenses(ctx.profile.get("expenses", {}))
    emi = total_emi(ctx.debts)
    savings_ratio = safe_divide(income - expenses - emi, income, 0)
    expense_ratio = safe_divide(expenses, income, 1)
    debt_burden = safe_divide(total_debt_outstanding(ctx.debts), income * 12, 0)

    emergency_required = (expenses + emi) * 6
    emergency_current = current_emergency_fund(ctx.assets)
    emergency_ratio = safe_divide(emergency_current, emergency_required, 0)

    asset_classes = {a.get("asset_class") for a in ctx.assets}
    diversification = min(len(asset_classes) / 4.0, 1.0)

    on_track_goals = sum(1 for g in ctx.goals if g.get("status") == "on_track")
    goal_score = safe_divide(on_track_goals, max(len(ctx.goals), 1), 0.5)

    components = {
        "savings_ratio": {
            "score": _score_component(savings_ratio, [(0.3, 100), (0.2, 80), (0.1, 60), (0.0, 30)]),
            "value": round(savings_ratio, 2),
        },
        "expense_ratio": {
            "score": _score_component(1 - expense_ratio, [(0.4, 100), (0.25, 80), (0.1, 60), (0.0, 30)]),
            "value": round(expense_ratio, 2),
        },
        "debt_burden": {
            "score": _score_component(1 - debt_burden, [(0.7, 100), (0.5, 80), (0.3, 60), (0.0, 30)]),
            "value": round(debt_burden, 2),
        },
        "emergency_fund": {
            "score": _score_component(emergency_ratio, [(1.0, 100), (0.75, 80), (0.5, 60), (0.0, 30)]),
            "value": round(emergency_ratio, 2),
        },
        "investment_readiness": {
            "score": 80 if savings_ratio > 0.15 and emergency_ratio > 0.5 else 50,
            "value": round(savings_ratio, 2),
        },
        "goal_preparedness": {
            "score": int(goal_score * 100),
            "value": round(goal_score, 2),
        },
        "diversification": {
            "score": int(diversification * 100),
            "value": round(diversification, 2),
        },
    }

    total = int(sum(item["score"] for item in components.values()) / len(components))
    explanation = [
        f"Savings ratio: {savings_ratio:.0%} of income after expenses and EMIs.",
        f"Expense ratio: {expense_ratio:.0%} of income.",
        f"Debt burden: {debt_burden:.2f} relative to annual income.",
        f"Emergency fund adequacy: {emergency_ratio:.0%} of recommended target.",
        f"Diversification across {len(asset_classes)} asset class(es).",
        f"Final score is the average of {len(components)} component scores.",
    ]

    return {"total_score": total, "components": components, "explanation": explanation}
