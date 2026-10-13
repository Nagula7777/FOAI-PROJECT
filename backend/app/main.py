"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.constants import FINANCIAL_DISCLAIMER
from app.config.settings import get_settings
from app.database.indexes import create_indexes
from app.database.mongodb import close_mongodb_connection, connect_to_mongodb
from app.routes import admin, ai, auth, goals, portfolio, profile, system
from app.seed.seed_data import seed_reference_data
from app.services.auth_service import seed_admin_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    await connect_to_mongodb()
    await create_indexes()
    await seed_admin_user(
        email=settings.seed_admin_email,
        password=settings.seed_admin_password,
        full_name=settings.seed_admin_name,
    )
    await seed_reference_data()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="AI-Based Personalized Financial Planning System",
    description=(
        "Academic decision-support API using classical AI techniques. "
        f"{FINANCIAL_DISCLAIMER}"
    ),
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(system.router)
app.include_router(profile.router)
app.include_router(goals.router)
app.include_router(ai.router)
app.include_router(portfolio.router)
app.include_router(admin.router)


@app.get("/")
async def root() -> dict:
    return {
        "message": "FOAI Financial Planning API",
        "disclaimer": FINANCIAL_DISCLAIMER,
        "docs": "/docs",
    }
