"""Seed default configuration and investment products."""

from datetime import datetime, timezone

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database


async def seed_reference_data() -> None:
    db = get_database()
    now = datetime.now(timezone.utc)

    if await db[COLLECTIONS["asset_classes"]].count_documents({}) == 0:
        await db[COLLECTIONS["asset_classes"]].insert_many(
            [
                {"code": "equity", "display_name": "Equity / Mutual Funds", "default_expected_return": 0.11, "default_risk_score": 0.75, "max_allocation_cap": 0.70},
                {"code": "bonds", "display_name": "Bonds", "default_expected_return": 0.07, "default_risk_score": 0.35, "max_allocation_cap": 0.60},
                {"code": "gold", "display_name": "Gold", "default_expected_return": 0.08, "default_risk_score": 0.45, "max_allocation_cap": 0.15},
                {"code": "cash", "display_name": "Cash / Low Risk", "default_expected_return": 0.04, "default_risk_score": 0.10, "max_allocation_cap": 0.40},
            ]
        )

    if await db[COLLECTIONS["investment_products"]].count_documents({}) == 0:
        await db[COLLECTIONS["investment_products"]].insert_many(
            [
                {"name": "Nifty 50 Index Fund", "asset_class": "equity", "risk_category": "moderate", "expected_return_assumption": 0.11, "liquidity": "high", "min_horizon_years": 5, "is_active": True},
                {"name": "Flexi-cap Fund", "asset_class": "equity", "risk_category": "high", "expected_return_assumption": 0.12, "liquidity": "high", "min_horizon_years": 5, "is_active": True},
                {"name": "Large-cap Fund", "asset_class": "equity", "risk_category": "moderate", "expected_return_assumption": 0.10, "liquidity": "high", "min_horizon_years": 5, "is_active": True},
                {"name": "Government Bonds", "asset_class": "bonds", "risk_category": "moderate", "expected_return_assumption": 0.07, "liquidity": "medium", "min_horizon_years": 2, "is_active": True},
                {"name": "Corporate Bonds", "asset_class": "bonds", "risk_category": "moderate", "expected_return_assumption": 0.08, "liquidity": "medium", "min_horizon_years": 3, "is_active": True},
                {"name": "Gold ETF", "asset_class": "gold", "risk_category": "moderate", "expected_return_assumption": 0.08, "liquidity": "high", "min_horizon_years": 3, "is_active": True},
                {"name": "Gold Fund", "asset_class": "gold", "risk_category": "moderate", "expected_return_assumption": 0.08, "liquidity": "medium", "min_horizon_years": 3, "is_active": True},
                {"name": "Liquid Fund", "asset_class": "cash", "risk_category": "moderate", "expected_return_assumption": 0.05, "liquidity": "high", "min_horizon_years": 0, "is_active": True},
            ]
        )

    if await db[COLLECTIONS["financial_rules"]].count_documents({}) == 0:
        await db[COLLECTIONS["financial_rules"]].insert_many(
            [
                {"rule_id": "EXPENSES_EXCEED_INCOME", "category": "priority", "condition": "expenses > income", "action": "set_financial_status_critical", "priority_weight": 100, "message_template": "Expenses exceed income.", "is_active": True},
                {"rule_id": "EMERGENCY_FUND_LOW", "category": "priority", "condition": "emergency_fund < required", "action": "prioritize_emergency_savings", "priority_weight": 85, "message_template": "Emergency fund is below recommended level.", "is_active": True},
                {"rule_id": "HIGH_INTEREST_DEBT", "category": "priority", "condition": "high_interest_debt", "action": "prioritize_debt_repayment", "priority_weight": 90, "message_template": "High-interest debt should be repaid first.", "is_active": True},
            ]
        )

    if await db[COLLECTIONS["constraint_configs"]].count_documents({}) == 0:
        await db[COLLECTIONS["constraint_configs"]].insert_one(
            {
                "config_name": "default",
                "max_equity_by_profile": {"conservative": 0.30, "moderate": 0.60, "aggressive": 0.80},
                "max_gold": 0.15,
                "min_cash": 0.05,
                "allocation_sum_tolerance": 0.01,
                "updated_at": now,
            }
        )
