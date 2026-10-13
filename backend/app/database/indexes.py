"""MongoDB index definitions."""

from app.config.constants import COLLECTIONS
from app.database.mongodb import get_database


async def create_indexes() -> None:
    db = get_database()

    await db[COLLECTIONS["users"]].create_index("email", unique=True)
    await db[COLLECTIONS["financial_profiles"]].create_index("user_id", unique=True)
    await db[COLLECTIONS["goals"]].create_index("user_id")
    await db[COLLECTIONS["debts"]].create_index("user_id")
    await db[COLLECTIONS["assets"]].create_index("user_id")
    await db[COLLECTIONS["recommendations"]].create_index("user_id")
    await db[COLLECTIONS["monthly_reports"]].create_index([("user_id", 1), ("report_month", 1)], unique=True)
    await db[COLLECTIONS["risk_assessments"]].create_index("user_id")
