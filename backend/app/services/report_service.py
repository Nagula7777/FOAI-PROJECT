"""Monthly report generation and PDF export."""

import io
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.config.constants import COLLECTIONS, FINANCIAL_DISCLAIMER
from app.database.mongodb import get_database
from app.services.ai_service import run_full_analysis
from app.services.goal_service import analyze_goal
from app.utils.financial_math import total_emi, total_expenses, total_income


async def generate_monthly_report(user_id: str) -> dict:
    now = datetime.now(timezone.utc)
    report_month = now.strftime("%Y-%m")

    existing = await get_database()[COLLECTIONS["monthly_reports"]].find_one(
        {"user_id": ObjectId(user_id), "report_month": report_month}
    )
    if existing:
        return _serialize_report(existing)

    profile = await get_database()[COLLECTIONS["financial_profiles"]].find_one(
        {"user_id": ObjectId(user_id)}
    )
    income = total_income(profile.get("income", {})) if profile else 0
    expenses = total_expenses(profile.get("expenses", {})) if profile else 0
    emi = 0
    async for debt in get_database()[COLLECTIONS["debts"]].find({"user_id": ObjectId(user_id)}):
        emi += float(debt.get("emi", 0))

    analysis = await run_full_analysis(user_id)
    previous = await get_database()[COLLECTIONS["monthly_reports"]].find_one(
        {"user_id": ObjectId(user_id)},
        sort=[("generated_at", -1)],
    )
    prev_score = previous.get("health_score", {}).get("current", analysis["health"]["total_score"]) if previous else analysis["health"]["total_score"]
    current_score = analysis["health"]["total_score"]

    goals = []
    async for goal in get_database()[COLLECTIONS["goals"]].find({"user_id": ObjectId(user_id)}):
        g_analysis = analyze_goal(goal)
        goals.append(
            {
                "name": goal["name"],
                "progress_pct": round(goal.get("current_amount", 0) / goal["target_amount"] * 100, 1),
                "status": g_analysis.status,
            }
        )

    report = {
        "user_id": ObjectId(user_id),
        "report_month": report_month,
        "financial_summary": {
            "income": income,
            "expenses": expenses,
            "savings": max(income - expenses - emi, 0),
            "emi_payments": emi,
            "investments": analysis["capacity"]["available_investment"],
        },
        "investment_summary": {
            "allocation": analysis["recommendation"]["allocation"],
            "monthly_investment": analysis["recommendation"]["monthly_investment_amount"],
        },
        "goal_progress": goals,
        "health_score": {
            "previous": prev_score,
            "current": current_score,
            "change": current_score - prev_score,
            "components": analysis["health"]["components"],
        },
        "ai_analysis": analysis["recommendation"]["explanations"][:5],
        "warnings": analysis["warnings"],
        "next_month_plan": {
            "expected_income": income,
            "recommended_expenses": expenses,
            "emergency_savings": analysis["emergency_fund"]["recommended_monthly_contribution"],
            "recommended_investment": analysis["capacity"]["available_investment"],
            "remaining_amount": max(
                income
                - expenses
                - emi
                - analysis["emergency_fund"]["recommended_monthly_contribution"]
                - analysis["capacity"]["available_investment"],
                0,
            ),
        },
        "generated_at": now,
    }

    result = await get_database()[COLLECTIONS["monthly_reports"]].insert_one(report)
    report["_id"] = result.inserted_id
    return _serialize_report(report)


async def list_reports(user_id: str) -> list[dict]:
    items = []
    async for doc in get_database()[COLLECTIONS["monthly_reports"]].find(
        {"user_id": ObjectId(user_id)}
    ).sort("generated_at", -1):
        items.append(
            {
                "id": str(doc["_id"]),
                "report_month": doc["report_month"],
                "generated_at": doc["generated_at"],
                "health_score": doc.get("health_score", {}).get("current", 0),
            }
        )
    return items


async def get_report(user_id: str, report_id: str) -> dict:
    doc = await get_database()[COLLECTIONS["monthly_reports"]].find_one(
        {"_id": ObjectId(report_id), "user_id": ObjectId(user_id)}
    )
    if not doc:
        raise HTTPException(status_code=404, detail="Report not found")
    return _serialize_report(doc)


def generate_report_pdf(report: dict) -> bytes:
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, f"Monthly Financial Report — {report['report_month']}")
    y -= 30
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, FINANCIAL_DISCLAIMER[:110] + "...")
    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Financial Summary")
    y -= 20
    pdf.setFont("Helvetica", 10)
    for key, value in report["financial_summary"].items():
        pdf.drawString(60, y, f"{key.replace('_', ' ').title()}: {value}")
        y -= 15
    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Financial Health Score: {report['health_score']['current']}/100")
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


def _serialize_report(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "report_month": doc["report_month"],
        "financial_summary": doc.get("financial_summary", {}),
        "investment_summary": doc.get("investment_summary", {}),
        "goal_progress": doc.get("goal_progress", []),
        "health_score": doc.get("health_score", {}),
        "ai_analysis": doc.get("ai_analysis", []),
        "warnings": doc.get("warnings", []),
        "next_month_plan": doc.get("next_month_plan", {}),
        "generated_at": doc.get("generated_at"),
    }
