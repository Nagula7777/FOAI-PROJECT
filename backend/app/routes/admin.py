"""Admin API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_admin
from app.schemas.admin import ConstraintUpdateRequest, ProductCreateRequest, RuleCreateRequest, UserAdminResponse
from app.schemas.auth import UserResponse
from app.services import admin_service

router = APIRouter(prefix="/api/admin", tags=["Admin"])


@router.get("/dashboard")
async def dashboard(_: Annotated[UserResponse, Depends(get_current_admin)]):
    from app.config.constants import COLLECTIONS
    from app.database.mongodb import get_database

    db = get_database()
    return {
        "users": await db[COLLECTIONS["users"]].count_documents({}),
        "recommendations": await db[COLLECTIONS["recommendations"]].count_documents({}),
        "reports": await db[COLLECTIONS["monthly_reports"]].count_documents({}),
        "products": await db[COLLECTIONS["investment_products"]].count_documents({}),
        "rules": await db[COLLECTIONS["financial_rules"]].count_documents({}),
    }


@router.get("/users", response_model=list[UserAdminResponse])
async def list_users(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.list_users()


@router.put("/users/{user_id}/status", response_model=UserAdminResponse)
async def toggle_user(
    user_id: str,
    is_active: bool,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.toggle_user_active(admin.id, user_id, is_active)


@router.get("/investment-products")
async def list_products(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.list_products()


@router.post("/investment-products")
async def create_product(
    payload: ProductCreateRequest,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.create_product(admin.id, payload)


@router.put("/investment-products/{product_id}")
async def update_product(
    product_id: str,
    payload: ProductCreateRequest,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.update_product(admin.id, product_id, payload)


@router.delete("/investment-products/{product_id}")
async def delete_product(
    product_id: str,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    await admin_service.delete_product(admin.id, product_id)
    return {"message": "Product deleted"}


@router.get("/asset-classes")
async def list_asset_classes(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.list_asset_classes()


@router.get("/financial-rules")
async def list_rules(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.list_rules()


@router.post("/financial-rules")
async def create_rule(
    payload: RuleCreateRequest,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.create_rule(admin.id, payload)


@router.put("/financial-rules/{rule_id}")
async def update_rule(
    rule_id: str,
    payload: RuleCreateRequest,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.update_rule(admin.id, rule_id, payload)


@router.delete("/financial-rules/{rule_id}")
async def delete_rule(
    rule_id: str,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    await admin_service.delete_rule(admin.id, rule_id)
    return {"message": "Rule deleted"}


@router.get("/constraint-config")
async def get_constraints(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.get_constraints()


@router.put("/constraint-config")
async def update_constraints(
    payload: ConstraintUpdateRequest,
    admin: Annotated[UserResponse, Depends(get_current_admin)],
):
    return await admin_service.update_constraints(admin.id, payload)


@router.get("/activity")
async def activity_log(_: Annotated[UserResponse, Depends(get_current_admin)]):
    return await admin_service.get_activity_log()
