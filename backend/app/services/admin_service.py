"""Admin business logic."""

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from fastapi import HTTPException

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.schemas.admin import (
    ConstraintUpdateRequest,
    ProductCreateRequest,
    RuleCreateRequest,
    UserAdminResponse,
)


async def log_activity(actor_id: str, action: str, entity: str, details: dict | None = None) -> None:
    await get_database()[COLLECTIONS["system_activity"]].insert_one(
        {
            "actor_id": ObjectId(actor_id),
            "action": action,
            "entity": entity,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc),
        }
    )


async def list_users() -> list[UserAdminResponse]:
    users = []
    async for doc in get_database()[COLLECTIONS["users"]].find().sort("created_at", -1):
        users.append(
            UserAdminResponse(
                id=str(doc["_id"]),
                email=doc["email"],
                full_name=doc["full_name"],
                role=doc["role"],
                is_active=doc.get("is_active", True),
                onboarding_completed=doc.get("onboarding_completed", False),
                created_at=doc["created_at"],
            )
        )
    return users


async def toggle_user_active(actor_id: str, user_id: str, is_active: bool) -> UserAdminResponse:
    result = await get_database()[COLLECTIONS["users"]].find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_active": is_active, "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    await log_activity(actor_id, "UPDATE_USER", "users", {"user_id": user_id, "is_active": is_active})
    return UserAdminResponse(
        id=str(result["_id"]),
        email=result["email"],
        full_name=result["full_name"],
        role=result["role"],
        is_active=result.get("is_active", True),
        onboarding_completed=result.get("onboarding_completed", False),
        created_at=result["created_at"],
    )


async def list_products() -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["investment_products"]].find().sort("name", 1):
        doc["id"] = str(doc["_id"])
        items.append(doc)
    return items


async def create_product(actor_id: str, payload: ProductCreateRequest) -> dict:
    doc = {**payload.model_dump(), "created_at": datetime.now(timezone.utc)}
    result = await get_database()[COLLECTIONS["investment_products"]].insert_one(doc)
    doc["_id"] = result.inserted_id
    doc["id"] = str(result.inserted_id)
    await log_activity(actor_id, "CREATE_PRODUCT", "investment_products", {"name": payload.name})
    return doc


async def update_product(actor_id: str, product_id: str, payload: ProductCreateRequest) -> dict:
    result = await get_database()[COLLECTIONS["investment_products"]].find_one_and_update(
        {"_id": ObjectId(product_id)},
        {"$set": payload.model_dump()},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    await log_activity(actor_id, "UPDATE_PRODUCT", "investment_products", {"product_id": product_id})
    result["id"] = str(result["_id"])
    return result


async def delete_product(actor_id: str, product_id: str) -> None:
    result = await get_database()[COLLECTIONS["investment_products"]].delete_one(
        {"_id": ObjectId(product_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    await log_activity(actor_id, "DELETE_PRODUCT", "investment_products", {"product_id": product_id})


async def list_rules() -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["financial_rules"]].find().sort("priority_weight", -1):
        doc["id"] = str(doc["_id"])
        items.append(doc)
    return items


async def create_rule(actor_id: str, payload: RuleCreateRequest) -> dict:
    doc = payload.model_dump()
    result = await get_database()[COLLECTIONS["financial_rules"]].insert_one(doc)
    doc["_id"] = result.inserted_id
    doc["id"] = str(result.inserted_id)
    await log_activity(actor_id, "CREATE_RULE", "financial_rules", {"rule_id": payload.rule_id})
    return doc


async def update_rule(actor_id: str, rule_id: str, payload: RuleCreateRequest) -> dict:
    result = await get_database()[COLLECTIONS["financial_rules"]].find_one_and_update(
        {"_id": ObjectId(rule_id)},
        {"$set": payload.model_dump()},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Rule not found")
    await log_activity(actor_id, "UPDATE_RULE", "financial_rules", {"rule_id": payload.rule_id})
    result["id"] = str(result["_id"])
    return result


async def delete_rule(actor_id: str, rule_id: str) -> None:
    result = await get_database()[COLLECTIONS["financial_rules"]].delete_one({"_id": ObjectId(rule_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Rule not found")
    await log_activity(actor_id, "DELETE_RULE", "financial_rules", {"rule_id": rule_id})


async def get_constraints() -> dict:
    doc = await get_database()[COLLECTIONS["constraint_configs"]].find_one({"config_name": "default"})
    if not doc:
        raise HTTPException(status_code=404, detail="Constraint config not found")
    doc["id"] = str(doc["_id"])
    return doc


async def update_constraints(actor_id: str, payload: ConstraintUpdateRequest) -> dict:
    result = await get_database()[COLLECTIONS["constraint_configs"]].find_one_and_update(
        {"config_name": "default"},
        {"$set": {**payload.model_dump(), "updated_at": datetime.now(timezone.utc)}},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Constraint config not found")
    await log_activity(actor_id, "UPDATE_CONSTRAINTS", "constraint_configs", payload.model_dump())
    result["id"] = str(result["_id"])
    return result


async def list_asset_classes() -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["asset_classes"]].find():
        doc["id"] = str(doc["_id"])
        items.append(doc)
    return items


async def get_activity_log(limit: int = 50) -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["system_activity"]].find().sort("timestamp", -1).limit(limit):
        items.append(
            {
                "id": str(doc["_id"]),
                "actor_id": str(doc["actor_id"]),
                "action": doc["action"],
                "entity": doc["entity"],
                "details": doc.get("details", {}),
                "timestamp": doc["timestamp"],
            }
        )
    return items
