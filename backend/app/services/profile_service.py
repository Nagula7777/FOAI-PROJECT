"""Financial profile, debt, and asset services."""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.schemas.profile import (
    AssetCreateRequest,
    AssetResponse,
    DebtCreateRequest,
    DebtResponse,
    ProfileResponse,
    ProfileUpdateRequest,
)


def _oid(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid id")
    return ObjectId(value)


async def get_profile(user_id: str) -> ProfileResponse | None:
    doc = await get_database()[COLLECTIONS["financial_profiles"]].find_one(
        {"user_id": _oid(user_id)}
    )
    if not doc:
        return None
    return ProfileResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        personal=doc["personal"],
        income=doc["income"],
        expenses=doc["expenses"],
        income_stability=doc.get("income_stability", "medium"),
        investment_experience=doc.get("investment_experience", "beginner"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


async def upsert_profile(user_id: str, payload: ProfileUpdateRequest) -> ProfileResponse:
    now = datetime.now(timezone.utc)
    db = get_database()
    update_doc = {
        "user_id": _oid(user_id),
        "personal": payload.personal.model_dump(),
        "income": payload.income.model_dump(),
        "expenses": payload.expenses.model_dump(),
        "income_stability": payload.income_stability,
        "investment_experience": payload.investment_experience,
        "updated_at": now,
    }
    existing = await db[COLLECTIONS["financial_profiles"]].find_one({"user_id": _oid(user_id)})
    if existing:
        await db[COLLECTIONS["financial_profiles"]].update_one(
            {"user_id": _oid(user_id)}, {"$set": update_doc}
        )
        doc = await db[COLLECTIONS["financial_profiles"]].find_one({"user_id": _oid(user_id)})
    else:
        update_doc["created_at"] = now
        result = await db[COLLECTIONS["financial_profiles"]].insert_one(update_doc)
        doc = await db[COLLECTIONS["financial_profiles"]].find_one({"_id": result.inserted_id})

    await db[COLLECTIONS["users"]].update_one(
        {"_id": _oid(user_id)}, {"$set": {"onboarding_completed": True, "updated_at": now}}
    )
    return ProfileResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        personal=doc["personal"],
        income=doc["income"],
        expenses=doc["expenses"],
        income_stability=doc.get("income_stability", "medium"),
        investment_experience=doc.get("investment_experience", "beginner"),
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


async def list_debts(user_id: str) -> list[DebtResponse]:
    items = []
    async for doc in get_database()[COLLECTIONS["debts"]].find({"user_id": _oid(user_id)}):
        items.append(_serialize_debt(doc))
    return items


async def create_debt(user_id: str, payload: DebtCreateRequest) -> DebtResponse:
    doc = {
        "user_id": _oid(user_id),
        **payload.model_dump(),
        "is_high_interest": payload.interest_rate >= 12,
        "created_at": datetime.now(timezone.utc),
    }
    result = await get_database()[COLLECTIONS["debts"]].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_debt(doc)


async def update_debt(user_id: str, debt_id: str, payload: DebtCreateRequest) -> DebtResponse:
    db = get_database()
    result = await db[COLLECTIONS["debts"]].find_one_and_update(
        {"_id": _oid(debt_id), "user_id": _oid(user_id)},
        {
            "$set": {
                **payload.model_dump(),
                "is_high_interest": payload.interest_rate >= 12,
            }
        },
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Debt not found")
    return _serialize_debt(result)


async def delete_debt(user_id: str, debt_id: str) -> None:
    result = await get_database()[COLLECTIONS["debts"]].delete_one(
        {"_id": _oid(debt_id), "user_id": _oid(user_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Debt not found")


async def list_assets(user_id: str) -> list[AssetResponse]:
    items = []
    async for doc in get_database()[COLLECTIONS["assets"]].find({"user_id": _oid(user_id)}):
        items.append(_serialize_asset(doc))
    return items


async def create_asset(user_id: str, payload: AssetCreateRequest) -> AssetResponse:
    doc = {
        "user_id": _oid(user_id),
        **payload.model_dump(),
        "created_at": datetime.now(timezone.utc),
    }
    result = await get_database()[COLLECTIONS["assets"]].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize_asset(doc)


async def update_asset(user_id: str, asset_id: str, payload: AssetCreateRequest) -> AssetResponse:
    result = await get_database()[COLLECTIONS["assets"]].find_one_and_update(
        {"_id": _oid(asset_id), "user_id": _oid(user_id)},
        {"$set": payload.model_dump()},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Asset not found")
    return _serialize_asset(result)


async def delete_asset(user_id: str, asset_id: str) -> None:
    result = await get_database()[COLLECTIONS["assets"]].delete_one(
        {"_id": _oid(asset_id), "user_id": _oid(user_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Asset not found")


def _serialize_debt(doc: dict) -> DebtResponse:
    return DebtResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        loan_type=doc["loan_type"],
        outstanding_amount=doc["outstanding_amount"],
        emi=doc["emi"],
        interest_rate=doc["interest_rate"],
        is_high_interest=doc.get("is_high_interest", doc["interest_rate"] >= 12),
    )


def _serialize_asset(doc: dict) -> AssetResponse:
    return AssetResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        asset_class=doc["asset_class"],
        name=doc["name"],
        current_value=doc["current_value"],
        is_emergency_fund=doc.get("is_emergency_fund", False),
    )
