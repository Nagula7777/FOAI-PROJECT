"""Goal management and achievement analysis."""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.schemas.goal import GoalAnalysisResponse, GoalCreateRequest, GoalResponse, GoalUpdateRequest
from app.utils.financial_math import future_value, months_until, required_monthly_contribution

ASSUMPTION_NOTE = (
    "Estimated future value uses configurable return assumptions and is not guaranteed."
)
DEFAULT_RETURN = 0.08


def _oid(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=400, detail="Invalid id")
    return ObjectId(value)


async def list_goals(user_id: str) -> list[GoalResponse]:
    items = []
    async for doc in get_database()[COLLECTIONS["goals"]].find({"user_id": _oid(user_id)}).sort(
        "priority", 1
    ):
        items.append(_serialize_goal(doc))
    return items


async def get_goal(user_id: str, goal_id: str) -> GoalResponse:
    doc = await get_database()[COLLECTIONS["goals"]].find_one(
        {"_id": _oid(goal_id), "user_id": _oid(user_id)}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    return _serialize_goal(doc)


async def create_goal(user_id: str, payload: GoalCreateRequest) -> GoalResponse:
    doc = {
        "user_id": _oid(user_id),
        **payload.model_dump(),
        "status": "at_risk",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await get_database()[COLLECTIONS["goals"]].insert_one(doc)
    doc["_id"] = result.inserted_id
    analysis = analyze_goal(doc)
    await get_database()[COLLECTIONS["goals"]].update_one(
        {"_id": result.inserted_id}, {"$set": {"status": analysis.status}}
    )
    doc["status"] = analysis.status
    return _serialize_goal(doc)


async def update_goal(user_id: str, goal_id: str, payload: GoalUpdateRequest) -> GoalResponse:
    updates = {k: v for k, v in payload.model_dump(exclude_none=True).items()}
    updates["updated_at"] = datetime.now(timezone.utc)
    doc = await get_database()[COLLECTIONS["goals"]].find_one_and_update(
        {"_id": _oid(goal_id), "user_id": _oid(user_id)},
        {"$set": updates},
        return_document=True,
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    analysis = analyze_goal(doc)
    await get_database()[COLLECTIONS["goals"]].update_one(
        {"_id": doc["_id"]}, {"$set": {"status": analysis.status}}
    )
    doc["status"] = analysis.status
    return _serialize_goal(doc)


async def delete_goal(user_id: str, goal_id: str) -> None:
    result = await get_database()[COLLECTIONS["goals"]].delete_one(
        {"_id": _oid(goal_id), "user_id": _oid(user_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found")


def analyze_goal(goal: dict, annual_return: float = DEFAULT_RETURN) -> GoalAnalysisResponse:
    current = float(goal.get("current_amount", 0))
    target = float(goal.get("target_amount", 0))
    monthly = float(goal.get("monthly_contribution", 0))
    months = months_until(goal.get("target_date"))
    remaining = max(target - current, 0)
    required = required_monthly_contribution(current, target, annual_return, months)
    estimated = future_value(current, monthly, annual_return, months)

    if estimated >= target * 0.98:
        status = "on_track"
    elif estimated >= target * 0.75:
        status = "at_risk"
    else:
        status = "unlikely"

    return GoalAnalysisResponse(
        goal_id=str(goal.get("_id", goal.get("id", ""))),
        current_amount=round(current, 2),
        target_amount=round(target, 2),
        remaining_amount=round(remaining, 2),
        months_remaining=round(months, 1),
        current_monthly_contribution=round(monthly, 2),
        required_monthly_contribution=round(required, 2),
        estimated_future_value=round(estimated, 2),
        status=status,
        assumption_note=ASSUMPTION_NOTE,
    )


async def analyze_goal_by_id(user_id: str, goal_id: str) -> GoalAnalysisResponse:
    doc = await get_database()[COLLECTIONS["goals"]].find_one(
        {"_id": _oid(goal_id), "user_id": _oid(user_id)}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Goal not found")
    return analyze_goal(doc)


def _serialize_goal(doc: dict) -> GoalResponse:
    return GoalResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        name=doc["name"],
        category=doc["category"],
        target_amount=doc["target_amount"],
        current_amount=doc.get("current_amount", 0),
        target_date=doc["target_date"],
        priority=doc.get("priority", 5),
        monthly_contribution=doc.get("monthly_contribution", 0),
        status=doc.get("status", "at_risk"),
    )
