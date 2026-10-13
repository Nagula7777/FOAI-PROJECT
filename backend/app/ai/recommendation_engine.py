"""Orchestrates the full classical AI recommendation pipeline."""

from datetime import datetime, timezone

from app.ai.constraints import derive_constraint_bounds
from app.ai.expert_system import evaluate_expert_system
from app.ai.explanation_builder import build_explanations
from app.ai.fuzzy_risk import evaluate_fuzzy_risk
from app.ai.genetic_optimizer import optimize_portfolio
from app.ai.health_scorer import calculate_health_score
from app.ai.types import AIExecutionTrace, FinancialContext
from app.config.constants import FINANCIAL_DISCLAIMER
from app.utils.financial_math import (
    current_emergency_fund,
    months_until,
    safe_divide,
    total_emi,
    total_expenses,
    total_income,
)


def _emergency_fund_analysis(ctx: FinancialContext) -> dict:
    essential = total_expenses(ctx.profile.get("expenses", {}))
    emi = total_emi(ctx.debts)
    dependents = ctx.profile.get("personal", {}).get("dependents", 0)
    stability = ctx.profile.get("income_stability", "medium")
    months = {"low": 9, "medium": 6, "high": 4}.get(stability, 6)
    required = (essential + emi) * months * (1 + 0.1 * dependents)
    current = current_emergency_fund(ctx.assets)
    remaining = max(required - current, 0)
    recommended_monthly = safe_divide(remaining, 12, 0)
    return {
        "required_amount": round(required, 2),
        "current_amount": round(current, 2),
        "remaining_amount": round(remaining, 2),
        "recommended_monthly_contribution": round(recommended_monthly, 2),
        "explanation": [
            f"Target based on {months} months of essential expenses plus EMIs.",
            f"Adjusted for {dependents} dependent(s) and {stability} income stability.",
        ],
    }


def _investment_capacity(ctx: FinancialContext, emergency: dict, expert_priorities: list[str]) -> dict:
    income = total_income(ctx.profile.get("income", {}))
    essential = total_expenses(ctx.profile.get("expenses", {}))
    emi = total_emi(ctx.debts)
    emergency_contribution = emergency["recommended_monthly_contribution"]
    if "emergency_savings" not in expert_priorities:
        emergency_contribution = min(emergency_contribution, income * 0.05)

    available = max(income - essential - emi - emergency_contribution, 0)
    conservative_cap = income * 0.35
    available = min(available, conservative_cap)

    breakdown = [
        f"Income: {income:.0f}",
        f"Essential expenses: -{essential:.0f}",
        f"Debt obligations (EMI): -{emi:.0f}",
        f"Emergency savings contribution: -{emergency_contribution:.0f}",
        f"Available investment capacity: {available:.0f}",
    ]
    return {
        "monthly_income": round(income, 2),
        "essential_expenses": round(essential, 2),
        "debt_obligations": round(emi, 2),
        "emergency_contribution": round(emergency_contribution, 2),
        "available_investment": round(available, 2),
        "breakdown": breakdown,
    }


def _select_products(allocation: dict, products: list[dict], monthly_amount: float) -> list[dict]:
    by_class: dict[str, list] = {}
    for product in products:
        if not product.get("is_active", True):
            continue
        cls = product.get("asset_class")
        by_class.setdefault(cls, []).append(product)

    mapping = {"equity": "equity", "bonds": "bonds", "gold": "gold", "cash": "cash"}
    selected = []
    for key, cls in mapping.items():
        pct = allocation.get(key, 0)
        if pct <= 0:
            continue
        options = by_class.get(cls, [])
        if not options:
            continue
        product = options[0]
        selected.append(
            {
                "product_id": str(product.get("_id", product.get("id", ""))),
                "name": product.get("name"),
                "asset_class": cls,
                "allocation_pct": round(pct, 4),
                "monthly_amount": round(monthly_amount * pct, 2),
            }
        )
    return selected


def run_recommendation_pipeline(
    ctx: FinancialContext,
    products: list[dict],
    questionnaire_score: float = 60,
    overrides: dict | None = None,
) -> dict:
    overrides = overrides or {}
    trace = AIExecutionTrace()

    expert = evaluate_expert_system(ctx)
    trace.expert = expert

    health = calculate_health_score(ctx)
    trace.health = health

    emergency = _emergency_fund_analysis(ctx)
    trace.emergency_fund = emergency

    capacity = _investment_capacity(ctx, emergency, expert.priorities)
    if overrides.get("monthly_investment_override") is not None:
        capacity["available_investment"] = float(overrides["monthly_investment_override"])
    trace.capacity = capacity

    risk = evaluate_fuzzy_risk(ctx, questionnaire_score)
    if overrides.get("risk_override"):
        dominant = overrides["risk_override"]
        risk = type(risk)(
            conservative=1.0 if dominant == "conservative" else 0.1,
            moderate=1.0 if dominant == "moderate" else 0.1,
            aggressive=1.0 if dominant == "aggressive" else 0.1,
            dominant=dominant,
            explanation=risk.explanation + [f"Risk profile overridden to {dominant} for scenario."],
        )
    trace.risk = risk

    bounds = derive_constraint_bounds(ctx, risk, capacity["available_investment"])
    trace.constraints = bounds

    allocation, ga_stats = optimize_portfolio(ctx, risk, bounds, expert.priorities)
    trace.ga_stats = ga_stats

    horizons = [months_until(g.get("target_date")) / 12.0 for g in ctx.goals if g.get("target_date")]
    horizon_years = max(horizons) if horizons else 5.0

    explanations = build_explanations(trace, allocation, horizon_years)
    trace.explanations = explanations

    monthly_amount = capacity["available_investment"]
    alloc_dict = allocation.as_dict()
    recommended_products = _select_products(alloc_dict, products, monthly_amount)

    return {
        "health": health,
        "emergency_fund": emergency,
        "capacity": capacity,
        "risk_profile": {
            "dominant": risk.dominant,
            "memberships": {
                "conservative": risk.conservative,
                "moderate": risk.moderate,
                "aggressive": risk.aggressive,
            },
            "explanation": risk.explanation,
        },
        "recommendation": {
            "generated_at": datetime.now(timezone.utc),
            "monthly_investment_amount": monthly_amount,
            "recommended_horizon_years": round(horizon_years, 1),
            "allocation": alloc_dict,
            "recommended_products": recommended_products,
            "explanations": explanations,
            "disclaimer": FINANCIAL_DISCLAIMER,
        },
        "trace": trace,
        "warnings": [],
    }
