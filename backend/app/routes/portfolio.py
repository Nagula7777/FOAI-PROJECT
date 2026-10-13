"""Portfolio, simulation, rebalancing, warnings, reports, investments."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.dependencies.auth import get_current_admin, get_current_user
from app.schemas.auth import UserResponse
from app.schemas.portfolio import WhatIfRequest
from app.services import portfolio_service, report_service, simulation_service
from app.services.context_builder import build_financial_context
from app.services.warning_service import detect_warnings
from app.services.ai_service import run_full_analysis, get_latest_recommendation

router = APIRouter(tags=["Portfolio & Reports"])


@router.get("/api/portfolio")
async def get_portfolio(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await portfolio_service.get_portfolio(current_user.id)


@router.get("/api/rebalancing")
async def rebalancing(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await portfolio_service.get_rebalancing(current_user.id)


@router.post("/api/simulation/what-if")
async def what_if(
    payload: WhatIfRequest,
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return await simulation_service.run_what_if(current_user.id, payload)


@router.get("/api/simulation/what-if")
async def list_what_if(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await simulation_service.list_scenarios(current_user.id)


@router.get("/api/simulation/what-if/{scenario_id}")
async def get_what_if(scenario_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    result = await simulation_service.get_scenario(current_user.id, scenario_id)
    if not result:
        raise HTTPException(status_code=404, detail="Scenario not found")
    return result


@router.get("/api/warnings")
async def warnings(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    ctx = await build_financial_context(current_user.id)
    rec = await get_latest_recommendation(current_user.id)
    if not rec:
        analysis = await run_full_analysis(current_user.id)
    else:
        analysis = {"emergency_fund": {}, "capacity": rec.get("investment_capacity_breakdown", {}), "recommendation": rec}
    return detect_warnings(ctx, analysis)


@router.get("/api/investment-products")
async def investment_products():
    items = []
    async for doc in get_database()[COLLECTIONS["investment_products"]].find({"is_active": True}):
        clean_doc = dict(doc)
        clean_doc["id"] = str(clean_doc["_id"])
        clean_doc.pop("_id", None)
        items.append(clean_doc)
    return items


@router.get("/api/reports/monthly")
async def list_reports(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await report_service.list_reports(current_user.id)


@router.post("/api/reports/monthly/generate")
async def generate_report(current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await report_service.generate_monthly_report(current_user.id)


@router.get("/api/reports/monthly/{report_id}")
async def get_report(report_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    return await report_service.get_report(current_user.id, report_id)


@router.get("/api/reports/monthly/{report_id}/pdf")
async def download_report_pdf(report_id: str, current_user: Annotated[UserResponse, Depends(get_current_user)]):
    report = await report_service.get_report(current_user.id, report_id)
    pdf_bytes = report_service.generate_report_pdf(report)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="report-{report["report_month"]}.pdf"'},
    )


@router.get("/api/admin/dashboard")
async def admin_dashboard(_: Annotated[UserResponse, Depends(get_current_admin)]):
    db = get_database()
    return {
        "users": await db[COLLECTIONS["users"]].count_documents({}),
        "recommendations": await db[COLLECTIONS["recommendations"]].count_documents({}),
        "reports": await db[COLLECTIONS["monthly_reports"]].count_documents({}),
    }
