"""What-if scenario simulation."""

from datetime import datetime, timezone

from bson import ObjectId

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.schemas.portfolio import WhatIfRequest
from app.services.ai_service import run_full_analysis


async def run_what_if(user_id: str, payload: WhatIfRequest) -> dict:
    overrides = {}
    if payload.monthly_income is not None:
        overrides["monthly_income"] = payload.monthly_income
    if payload.expense_multiplier is not None:
        overrides["expense_multiplier"] = payload.expense_multiplier
    if payload.goal_amount_override is not None:
        overrides["goal_amount_override"] = payload.goal_amount_override
    if payload.goal_date_override is not None:
        overrides["goal_date_override"] = payload.goal_date_override
    if payload.monthly_investment_override is not None:
        overrides["monthly_investment_override"] = payload.monthly_investment_override
    if payload.risk_override is not None:
        overrides["risk_override"] = payload.risk_override

    baseline = await run_full_analysis(user_id)
    scenario = await run_full_analysis(user_id, overrides=overrides)

    comparison = {
        "capacity_delta": round(
            scenario["capacity"]["available_investment"]
            - baseline["capacity"]["available_investment"],
            2,
        ),
        "health_delta": scenario["health"]["total_score"] - baseline["health"]["total_score"],
        "allocation_changes": {
            k: round(scenario["recommendation"]["allocation"].get(k, 0) - baseline["recommendation"]["allocation"].get(k, 0), 4)
            for k in baseline["recommendation"]["allocation"]
        },
    }

    saved = {
        "user_id": ObjectId(user_id),
        "name": payload.name,
        "input_overrides": payload.model_dump(exclude_none=True),
        "baseline_snapshot": baseline,
        "scenario_result": scenario,
        "comparison": comparison,
        "created_at": datetime.now(timezone.utc),
    }
    result = await get_database()[COLLECTIONS["what_if_scenarios"]].insert_one(saved)

    return {
        "id": str(result.inserted_id),
        "name": payload.name,
        "baseline": baseline,
        "scenario": scenario,
        "comparison": comparison,
    }


async def list_scenarios(user_id: str) -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["what_if_scenarios"]].find(
        {"user_id": ObjectId(user_id)}
    ).sort("created_at", -1):
        items.append(
            {
                "id": str(doc["_id"]),
                "name": doc["name"],
                "created_at": doc["created_at"],
                "comparison": doc.get("comparison", {}),
            }
        )
    return items


async def get_scenario(user_id: str, scenario_id: str) -> dict:
    doc = await get_database()[COLLECTIONS["what_if_scenarios"]].find_one(
        {"_id": ObjectId(scenario_id), "user_id": ObjectId(user_id)}
    )
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "baseline": doc.get("baseline_snapshot", {}),
        "scenario": doc.get("scenario_result", {}),
        "comparison": doc.get("comparison", {}),
    }
