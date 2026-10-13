"""AI algorithm unit tests."""

from app.ai.expert_system import evaluate_expert_system
from app.ai.fuzzy_risk import evaluate_fuzzy_risk
from app.ai.constraints import derive_constraint_bounds, is_feasible
from app.ai.health_scorer import calculate_health_score
from app.ai.types import FinancialContext, PortfolioAllocation, RiskProfile


def _sample_context(**kwargs):
    defaults = {
        "user_id": "test",
        "profile": {
            "personal": {"age": 32, "employment_status": "employed", "dependents": 1},
            "income": {"monthly_income": 80000, "other_monthly_income": 5000},
            "expenses": {"rent": 15000, "food": 8000, "transportation": 3000, "other": 2000},
            "income_stability": "medium",
            "investment_experience": "beginner",
        },
        "debts": [{"emi": 10000, "interest_rate": 14, "outstanding_amount": 200000}],
        "assets": [{"asset_class": "cash", "current_value": 50000, "is_emergency_fund": True}],
        "goals": [],
        "risk_assessment": None,
        "constraint_config": {
            "max_equity_by_profile": {"conservative": 0.30, "moderate": 0.60, "aggressive": 0.80},
            "max_gold": 0.15,
            "min_cash": 0.05,
        },
        "asset_classes": [],
        "rules": [],
    }
    defaults.update(kwargs)
    return FinancialContext(**defaults)


def test_expert_system_detects_emergency_fund_gap():
    result = evaluate_expert_system(_sample_context())
    assert any(c.rule_id == "EMERGENCY_FUND_LOW" for c in result.conclusions)


def test_fuzzy_risk_returns_memberships():
    ctx = _sample_context()
    risk = evaluate_fuzzy_risk(ctx, questionnaire_score=65)
    assert 0.99 <= risk.conservative + risk.moderate + risk.aggressive <= 1.01
    assert risk.dominant in {"conservative", "moderate", "aggressive"}


def test_health_score_range():
    result = calculate_health_score(_sample_context())
    assert 0 <= result["total_score"] <= 100
    assert len(result["components"]) >= 5


def test_constraint_feasibility():
    ctx = _sample_context()
    risk = RiskProfile(0.2, 0.6, 0.2, "moderate", [])
    bounds = derive_constraint_bounds(ctx, risk, 10000)
    allocation = PortfolioAllocation(equity=0.5, bonds=0.3, gold=0.1, cash=0.1)
    assert is_feasible(allocation, bounds, tolerance=0.03)
