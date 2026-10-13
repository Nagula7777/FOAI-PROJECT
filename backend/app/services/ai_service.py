"""AI analysis orchestration and persistence."""

from datetime import datetime, timezone

from bson import ObjectId

from app.ai.recommendation_engine import run_recommendation_pipeline
from app.config.constants import COLLECTIONS, FINANCIAL_DISCLAIMER
from app.database.mongodb import get_database
from app.services.context_builder import build_financial_context
from app.services.warning_service import detect_warnings


async def _get_products() -> list[dict]:
    products = []
    async for product in get_database()[COLLECTIONS["investment_products"]].find({"is_active": True}):
        products.append(product)
    return products


async def run_full_analysis(user_id: str, overrides: dict | None = None) -> dict:
    ctx = await build_financial_context(user_id, overrides)
    risk_doc = await get_database()[COLLECTIONS["risk_assessments"]].find_one(
        {"user_id": ObjectId(user_id)}, sort=[("assessed_at", -1)]
    )
    questionnaire_score = risk_doc["questionnaire_score"] if risk_doc else 60

    result = run_recommendation_pipeline(
        ctx,
        await _get_products(),
        questionnaire_score=questionnaire_score,
        overrides=overrides,
    )

    warnings = detect_warnings(ctx, result)
    result["warnings"] = warnings

    rec = result["recommendation"]
    saved = {
        "user_id": ObjectId(user_id),
        "generated_at": rec["generated_at"],
        "monthly_investment_amount": rec["monthly_investment_amount"],
        "recommended_horizon_years": rec["recommended_horizon_years"],
        "allocation": rec["allocation"],
        "recommended_products": rec["recommended_products"],
        "risk_profile": result["risk_profile"],
        "investment_capacity_breakdown": result["capacity"],
        "explanations": rec["explanations"],
        "ai_trace": {
            "ga_generations": result["trace"].ga_stats.get("generations"),
            "best_fitness": result["trace"].ga_stats.get("best_fitness"),
        },
        "disclaimer": FINANCIAL_DISCLAIMER,
    }
    insert_result = await get_database()[COLLECTIONS["recommendations"]].insert_one(saved)
    rec_id = str(insert_result.inserted_id)

    await _upsert_portfolio_target(user_id, rec["allocation"])

    return {
        "health": result["health"],
        "emergency_fund": result["emergency_fund"],
        "capacity": result["capacity"],
        "risk_profile": result["risk_profile"],
        "recommendation": {**rec, "id": rec_id},
        "warnings": warnings,
        "trace_summary": result["trace"].ga_stats,
    }


async def _upsert_portfolio_target(user_id: str, target_allocation: dict) -> None:
    db = get_database()
    existing = await db[COLLECTIONS["portfolios"]].find_one({"user_id": ObjectId(user_id)})
    if existing:
        await db[COLLECTIONS["portfolios"]].update_one(
            {"user_id": ObjectId(user_id)},
            {"$set": {"target_allocation": target_allocation, "last_updated": datetime.now(timezone.utc)}},
        )
    else:
        await db[COLLECTIONS["portfolios"]].insert_one(
            {
                "user_id": ObjectId(user_id),
                "current_allocation": {"equity": 0, "bonds": 0, "gold": 0, "cash": 1},
                "target_allocation": target_allocation,
                "drift_threshold": 0.05,
                "last_updated": datetime.now(timezone.utc),
            }
        )


async def get_recommendation_by_id(user_id: str, recommendation_id: str) -> dict | None:
    doc = await get_database()[COLLECTIONS["recommendations"]].find_one(
        {"_id": ObjectId(recommendation_id), "user_id": ObjectId(user_id)}
    )
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "generated_at": doc["generated_at"],
        "monthly_investment_amount": doc["monthly_investment_amount"],
        "recommended_horizon_years": doc["recommended_horizon_years"],
        "allocation": doc["allocation"],
        "recommended_products": doc.get("recommended_products", []),
        "risk_profile": doc.get("risk_profile", {}),
        "investment_capacity_breakdown": doc.get("investment_capacity_breakdown", {}),
        "explanations": doc.get("explanations", []),
        "disclaimer": doc.get("disclaimer", FINANCIAL_DISCLAIMER),
    }


async def get_latest_recommendation(user_id: str) -> dict | None:
    doc = await get_database()[COLLECTIONS["recommendations"]].find_one(
        {"user_id": ObjectId(user_id)}, sort=[("generated_at", -1)]
    )
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "generated_at": doc["generated_at"],
        "monthly_investment_amount": doc["monthly_investment_amount"],
        "recommended_horizon_years": doc["recommended_horizon_years"],
        "allocation": doc["allocation"],
        "recommended_products": doc.get("recommended_products", []),
        "risk_profile": doc.get("risk_profile", {}),
        "investment_capacity_breakdown": doc.get("investment_capacity_breakdown", {}),
        "explanations": doc.get("explanations", []),
        "disclaimer": doc.get("disclaimer", FINANCIAL_DISCLAIMER),
    }


async def run_portfolio_optimize(user_id: str) -> dict:
    ctx = await build_financial_context(user_id)
    from app.services.context_builder import build_financial_context
    from app.ai.expert_system import evaluate_expert_system
    from app.ai.fuzzy_risk import evaluate_fuzzy_risk
    from app.ai.recommendation_engine import _emergency_fund_analysis, _investment_capacity
    from app.ai.constraints import derive_constraint_bounds
    from app.ai.genetic_optimizer import optimize_portfolio

    risk_doc = await get_database()[COLLECTIONS["risk_assessments"]].find_one(
        {"user_id": ObjectId(user_id)}, sort=[("assessed_at", -1)]
    )
    questionnaire_score = risk_doc["questionnaire_score"] if risk_doc else 60
    expert = evaluate_expert_system(ctx)
    emergency = _emergency_fund_analysis(ctx)
    capacity = _investment_capacity(ctx, emergency, expert.priorities)
    risk = evaluate_fuzzy_risk(ctx, questionnaire_score)
    bounds = derive_constraint_bounds(ctx, risk, capacity["available_investment"])
    allocation, ga_stats = optimize_portfolio(ctx, risk, bounds, expert.priorities)
    return {
        "allocation": allocation.as_dict(),
        "fitness": ga_stats.get("best_fitness"),
        "generations": ga_stats.get("generations"),
        "monthly_investment": capacity["available_investment"],
    }
