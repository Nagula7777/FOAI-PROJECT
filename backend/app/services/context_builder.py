"""Build FinancialContext from database documents."""

from bson import ObjectId

from app.ai.types import FinancialContext
from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database


async def build_financial_context(user_id: str, overrides: dict | None = None) -> FinancialContext:
    db = get_database()
    overrides = overrides or {}

    profile = await db[COLLECTIONS["financial_profiles"]].find_one({"user_id": ObjectId(user_id)})
    if not profile and not overrides.get("skip_profile_check"):
        profile = {
            "personal": {"age": 30, "employment_status": "employed", "dependents": 0},
            "income": {"monthly_income": 0, "other_monthly_income": 0},
            "expenses": {},
            "income_stability": "medium",
            "investment_experience": "beginner",
        }

    if overrides.get("monthly_income") is not None:
        profile = dict(profile or {})
        profile["income"] = dict(profile.get("income", {}))
        profile["income"]["monthly_income"] = overrides["monthly_income"]

    if overrides.get("expense_multiplier") is not None:
        profile = dict(profile or {})
        multiplier = overrides["expense_multiplier"]
        profile["expenses"] = {
            k: float(v) * multiplier for k, v in profile.get("expenses", {}).items()
        }

    debts = []
    async for debt in db[COLLECTIONS["debts"]].find({"user_id": ObjectId(user_id)}):
        debt["id"] = str(debt["_id"])
        debts.append(debt)

    assets = []
    async for asset in db[COLLECTIONS["assets"]].find({"user_id": ObjectId(user_id)}):
        asset["id"] = str(asset["_id"])
        assets.append(asset)

    goals = []
    async for goal in db[COLLECTIONS["goals"]].find({"user_id": ObjectId(user_id)}).sort("priority", 1):
        if overrides.get("goal_amount_override") is not None:
            goal = dict(goal)
            goal["target_amount"] = overrides["goal_amount_override"]
        if overrides.get("goal_date_override") is not None:
            goal = dict(goal)
            goal["target_date"] = overrides["goal_date_override"]
        goal["id"] = str(goal["_id"])
        goals.append(goal)

    risk = await db[COLLECTIONS["risk_assessments"]].find_one(
        {"user_id": ObjectId(user_id)},
        sort=[("assessed_at", -1)],
    )

    constraint_config = await db[COLLECTIONS["constraint_configs"]].find_one({"config_name": "default"})
    if not constraint_config:
        constraint_config = {
            "max_equity_by_profile": {"conservative": 0.30, "moderate": 0.60, "aggressive": 0.80},
            "max_gold": 0.15,
            "min_cash": 0.05,
        }

    asset_classes = []
    async for item in db[COLLECTIONS["asset_classes"]].find():
        asset_classes.append(item)

    rules = []
    async for rule in db[COLLECTIONS["financial_rules"]].find({"is_active": True}):
        rules.append(rule)

    return_assumptions = {}
    for item in asset_classes:
        return_assumptions[item.get("code", "")] = float(item.get("default_expected_return", 0.08))

    return FinancialContext(
        user_id=user_id,
        profile=profile or {},
        debts=debts,
        assets=assets,
        goals=goals,
        risk_assessment=risk,
        constraint_config=constraint_config,
        asset_classes=asset_classes,
        rules=rules,
        return_assumptions=return_assumptions,
    )
