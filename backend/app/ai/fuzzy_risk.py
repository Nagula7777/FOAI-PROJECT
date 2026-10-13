"""Fuzzy logic risk profiling using scikit-fuzzy."""

import numpy as np
import skfuzzy as fuzz

from app.ai.types import FinancialContext, RiskProfile
from app.utils.financial_math import safe_divide, total_debt_outstanding, total_income


def _stability_score(value: str) -> float:
    return {"low": 0.2, "medium": 0.55, "high": 0.85}.get(value, 0.55)


def _experience_score(value: str) -> float:
    return {"none": 0.2, "beginner": 0.4, "intermediate": 0.65, "advanced": 0.85}.get(value, 0.4)


def evaluate_fuzzy_risk(ctx: FinancialContext, questionnaire_score: float) -> RiskProfile:
    personal = ctx.profile.get("personal", {})
    age = float(personal.get("age", 30))
    income = total_income(ctx.profile.get("income", {}))
    debt_ratio = safe_divide(total_debt_outstanding(ctx.debts), income * 12, default=0.0)

    horizons = []
    for goal in ctx.goals:
        target = goal.get("target_date")
        if target:
            from app.utils.financial_math import months_until

            horizons.append(months_until(target) / 12.0)
    horizon_years = max(horizons) if horizons else 5.0

    age_norm = np.clip((65 - age) / 45, 0, 1)
    stability_norm = _stability_score(ctx.profile.get("income_stability", "medium"))
    horizon_norm = np.clip(horizon_years / 20.0, 0, 1)
    debt_norm = np.clip(1 - debt_ratio, 0, 1)
    experience_norm = _experience_score(ctx.profile.get("investment_experience", "beginner"))
    questionnaire_norm = np.clip(questionnaire_score / 100.0, 0, 1)

    risk_input = np.clip(
        0.15 * age_norm
        + 0.15 * stability_norm
        + 0.20 * horizon_norm
        + 0.10 * debt_norm
        + 0.10 * experience_norm
        + 0.30 * questionnaire_norm,
        0,
        1,
    )

    x = np.linspace(0, 1, 101)
    conservative = float(fuzz.interp_membership(x, fuzz.trapmf(x, [0, 0, 0.25, 0.45]), risk_input))
    moderate = float(fuzz.interp_membership(x, fuzz.trimf(x, [0.25, 0.5, 0.75]), risk_input))
    aggressive = float(fuzz.interp_membership(x, fuzz.trapmf(x, [0.55, 0.75, 1, 1]), risk_input))

    total = conservative + moderate + aggressive
    if total > 0:
        conservative /= total
        moderate /= total
        aggressive /= total

    dominant = max(
        ("conservative", conservative),
        ("moderate", moderate),
        ("aggressive", aggressive),
        key=lambda item: item[1],
    )[0]

    explanation = [
        f"Age factor contributes to a {'longer' if age < 45 else 'shorter'} investment horizon preference.",
        f"Income stability is assessed as {ctx.profile.get('income_stability', 'medium')}.",
        f"Investment horizon inferred at approximately {horizon_years:.1f} years.",
        f"Debt burden normalized score: {debt_norm:.2f}.",
        f"Questionnaire normalized score: {questionnaire_norm:.2f}.",
        f"Fuzzy memberships — Conservative: {conservative:.2f}, Moderate: {moderate:.2f}, Aggressive: {aggressive:.2f}.",
    ]

    return RiskProfile(
        conservative=round(conservative, 2),
        moderate=round(moderate, 2),
        aggressive=round(aggressive, 2),
        dominant=dominant,
        explanation=explanation,
    )
