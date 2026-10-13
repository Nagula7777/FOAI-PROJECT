"""Deterministic financial calculations (no ML)."""

from datetime import datetime, timezone
from typing import Iterable


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    if denominator == 0:
        return default
    return numerator / denominator


def total_expenses(expenses: dict) -> float:
    return sum(float(v or 0) for v in expenses.values())


def total_income(income: dict) -> float:
    return float(income.get("monthly_income", 0) or 0) + float(
        income.get("other_monthly_income", 0) or 0
    )


def total_emi(debts: Iterable[dict]) -> float:
    return sum(float(d.get("emi", 0) or 0) for d in debts)


def total_debt_outstanding(debts: Iterable[dict]) -> float:
    return sum(float(d.get("outstanding_amount", 0) or 0) for d in debts)


def asset_total_by_class(assets: Iterable[dict]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for asset in assets:
        cls = asset.get("asset_class", "other")
        totals[cls] = totals.get(cls, 0.0) + float(asset.get("current_value", 0) or 0)
    return totals


def current_emergency_fund(assets: Iterable[dict]) -> float:
    return sum(
        float(a.get("current_value", 0) or 0)
        for a in assets
        if a.get("is_emergency_fund") or a.get("asset_class") == "cash"
    )


def months_until(target_date: datetime | str) -> float:
    if isinstance(target_date, str):
        target_date = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
    if target_date.tzinfo is None:
        target_date = target_date.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta_days = (target_date - now).days
    return max(delta_days / 30.4375, 0.0)


def future_value(
    present: float,
    monthly_contribution: float,
    annual_return: float,
    months: float,
) -> float:
    if months <= 0:
        return present + monthly_contribution
    monthly_rate = annual_return / 12.0
    if abs(monthly_rate) < 1e-9:
        return present + monthly_contribution * months
    growth = (1 + monthly_rate) ** months
    return present * growth + monthly_contribution * ((growth - 1) / monthly_rate)


def required_monthly_contribution(
    current: float,
    target: float,
    annual_return: float,
    months: float,
) -> float:
    if months <= 0:
        return max(target - current, 0.0)
    remaining = max(target - current, 0.0)
    monthly_rate = annual_return / 12.0
    if abs(monthly_rate) < 1e-9:
        return remaining / months
    growth = (1 + monthly_rate) ** months
    denominator = (growth - 1) / monthly_rate
    if denominator <= 0:
        return remaining / months
    fv_current = current * growth
    needed = target - fv_current
    return max(needed / denominator, 0.0)
