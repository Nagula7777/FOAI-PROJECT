"""Risk assessment persistence."""

from datetime import datetime, timezone

from bson import ObjectId

from app.ai.fuzzy_risk import evaluate_fuzzy_risk
from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database
from app.schemas.risk import RiskAssessmentRequest, RiskAssessmentResponse
from app.services.context_builder import build_financial_context


async def submit_risk_assessment(user_id: str, payload: RiskAssessmentRequest) -> RiskAssessmentResponse:
    responses = payload.model_dump()
    questionnaire_score = int(sum(responses.values()) / len(responses) * 20)

    ctx = await build_financial_context(user_id)
    risk = evaluate_fuzzy_risk(ctx, questionnaire_score)

    doc = {
        "user_id": ObjectId(user_id),
        "questionnaire_responses": responses,
        "questionnaire_score": questionnaire_score,
        "fuzzy_output": {
            "conservative": risk.conservative,
            "moderate": risk.moderate,
            "aggressive": risk.aggressive,
        },
        "dominant_profile": risk.dominant,
        "explanation": risk.explanation,
        "assessed_at": datetime.now(timezone.utc),
    }
    result = await get_database()[COLLECTIONS["risk_assessments"]].insert_one(doc)
    return RiskAssessmentResponse(
        id=str(result.inserted_id),
        questionnaire_score=questionnaire_score,
        fuzzy_output=doc["fuzzy_output"],
        dominant_profile=risk.dominant,
        explanation=risk.explanation,
        assessed_at=doc["assessed_at"],
    )


async def get_latest_risk_assessment(user_id: str) -> RiskAssessmentResponse | None:
    doc = await get_database()[COLLECTIONS["risk_assessments"]].find_one(
        {"user_id": ObjectId(user_id)},
        sort=[("assessed_at", -1)],
    )
    if not doc:
        return None
    return RiskAssessmentResponse(
        id=str(doc["_id"]),
        questionnaire_score=doc["questionnaire_score"],
        fuzzy_output=doc["fuzzy_output"],
        dominant_profile=doc["dominant_profile"],
        explanation=doc.get("explanation", []),
        assessed_at=doc["assessed_at"],
    )
