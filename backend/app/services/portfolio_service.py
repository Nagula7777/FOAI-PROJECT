"""Portfolio and rebalancing services."""

from datetime import datetime, timezone

from bson import ObjectId

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.utils.financial_math import asset_total_by_class


async def get_portfolio(user_id: str) -> dict:
    doc = await get_database()[COLLECTIONS["portfolios"]].find_one({"user_id": ObjectId(user_id)})
    assets = []
    async for asset in get_database()[COLLECTIONS["assets"]].find({"user_id": ObjectId(user_id)}):
        assets.append(asset)

    totals = asset_total_by_class(assets)
    total_value = sum(totals.values()) or 1
    current = {
        "equity": totals.get("equity", 0) / total_value,
        "bonds": totals.get("bonds", 0) / total_value,
        "gold": totals.get("gold", 0) / total_value,
        "cash": totals.get("cash", 0) / total_value,
    }

    target = doc.get("target_allocation", current) if doc else current
    drift = {k: round(current.get(k, 0) - target.get(k, 0), 4) for k in target}
    threshold = doc.get("drift_threshold", 0.05) if doc else 0.05
    needs_rebalancing = any(abs(v) > threshold for v in drift.values())

    return {
        "current_allocation": {k: round(v, 4) for k, v in current.items()},
        "target_allocation": target,
        "drift": drift,
        "needs_rebalancing": needs_rebalancing,
    }


async def get_rebalancing(user_id: str) -> dict:
    portfolio = await get_portfolio(user_id)
    suggestions = []
    for asset, drift in portfolio["drift"].items():
        if abs(drift) > 0.05:
            direction = "reduce" if drift > 0 else "increase"
            suggestions.append(f"{direction.title()} {asset} allocation by {abs(drift):.0%}.")

    explanation = [
        "Rebalancing keeps your portfolio aligned with your AI target allocation.",
        "Drift can occur when asset classes grow at different rates.",
    ]
    if not suggestions:
        explanation.append("Current allocation is within acceptable drift limits.")

    return {
        **portfolio,
        "suggestions": suggestions,
        "explanation": explanation,
    }
