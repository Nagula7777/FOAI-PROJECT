"""Rule-based expert system for financial reasoning."""

from app.ai.types import ExpertConclusion, ExpertSystemResult, FinancialContext
from app.utils.financial_math import (
    current_emergency_fund,
    total_debt_outstanding,
    total_emi,
    total_expenses,
    total_income,
)


def _required_emergency_fund(ctx: FinancialContext) -> float:
    essential = total_expenses(ctx.profile.get("expenses", {}))
    emi = total_emi(ctx.debts)
    dependents = ctx.profile.get("personal", {}).get("dependents", 0)
    stability = ctx.profile.get("income_stability", "medium")
    months = {"low": 9, "medium": 6, "high": 4}.get(stability, 6)
    multiplier = 1 + 0.1 * dependents
    return (essential + emi) * months * multiplier


def evaluate_expert_system(ctx: FinancialContext) -> ExpertSystemResult:
    income = total_income(ctx.profile.get("income", {}))
    expenses = total_expenses(ctx.profile.get("expenses", {}))
    emi = total_emi(ctx.debts)
    debt_total = total_debt_outstanding(ctx.debts)
    emergency_current = current_emergency_fund(ctx.assets)
    emergency_required = _required_emergency_fund(ctx)

    conclusions: list[ExpertConclusion] = []
    priorities: list[str] = []
    warnings: list[str] = []
    financial_status = "stable"

    if expenses + emi > income:
        financial_status = "critical"
        conclusions.append(
            ExpertConclusion(
                rule_id="EXPENSES_EXCEED_INCOME",
                message=f"Expenses and EMIs ({expenses + emi:.0f}) exceed income ({income:.0f}).",
                priority="critical",
                weight=100,
            )
        )
        priorities.append("reduce_expenses")

    high_interest_debts = [
        d for d in ctx.debts if float(d.get("interest_rate", 0)) >= 12 or d.get("is_high_interest")
    ]
    if high_interest_debts:
        conclusions.append(
            ExpertConclusion(
                rule_id="HIGH_INTEREST_DEBT",
                message="High-interest debt detected. Prioritize debt repayment before aggressive investing.",
                priority="high",
                weight=90,
            )
        )
        priorities.append("debt_repayment")

    if emergency_current < emergency_required:
        gap = emergency_required - emergency_current
        conclusions.append(
            ExpertConclusion(
                rule_id="EMERGENCY_FUND_LOW",
                message=f"Emergency fund gap of {gap:.0f}. Build emergency savings before higher-risk investing.",
                priority="high",
                weight=85,
            )
        )
        priorities.append("emergency_savings")

    short_term_goals = [g for g in ctx.goals if g.get("category") in {"vehicle", "travel", "marriage"}]
    if short_term_goals:
        conclusions.append(
            ExpertConclusion(
                rule_id="SHORT_TERM_GOALS",
                message="Short-term goals present. Favor capital preservation and liquidity.",
                priority="medium",
                weight=70,
            )
        )
        priorities.append("capital_preservation")

    if debt_total > income * 12:
        conclusions.append(
            ExpertConclusion(
                rule_id="HIGH_DEBT_BURDEN",
                message="Debt burden exceeds 12 months of income.",
                priority="high",
                weight=80,
            )
        )
        warnings.append("Debt burden is high relative to income.")

    if not priorities:
        priorities.append("investment_growth")

    for rule in ctx.rules:
        if not rule.get("is_active", True):
            continue
        rule_id = rule.get("rule_id", "")
        if rule_id in {c.rule_id for c in conclusions}:
            continue
        condition = rule.get("condition", "")
        if condition == "expenses > income" and expenses > income:
            conclusions.append(
                ExpertConclusion(
                    rule_id=rule_id,
                    message=rule.get("message_template", "Rule triggered"),
                    priority=rule.get("category", "medium"),
                    weight=int(rule.get("priority_weight", 50)),
                )
            )

    return ExpertSystemResult(
        financial_status=financial_status,
        priorities=priorities,
        conclusions=conclusions,
        warnings=warnings,
    )
