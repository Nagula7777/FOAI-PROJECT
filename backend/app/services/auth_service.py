"""Authentication business logic."""

from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.config.constants import ADMIN_ROLE, COLLECTIONS, USER_ROLE
from app.database.mongodb import get_database
from app.schemas.auth import TokenResponse, UserLoginRequest, UserRegisterRequest, UserResponse
from app.utils.security import create_access_token, hash_password, verify_password


def _serialize_user(document: dict) -> UserResponse:
    return UserResponse(
        id=str(document["_id"]),
        email=document["email"],
        full_name=document["full_name"],
        role=document["role"],
        onboarding_completed=document.get("onboarding_completed", False),
        created_at=document["created_at"],
    )


async def register_user(payload: UserRegisterRequest) -> TokenResponse:
    db = get_database()
    users = db[COLLECTIONS["users"]]

    existing = await users.find_one({"email": payload.email.lower()})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    now = datetime.now(timezone.utc)
    user_doc = {
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "full_name": payload.full_name.strip(),
        "role": USER_ROLE,
        "is_active": True,
        "onboarding_completed": False,
        "created_at": now,
        "updated_at": now,
    }

    result = await users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    token = create_access_token({"sub": str(result.inserted_id), "role": USER_ROLE})
    return TokenResponse(access_token=token, user=_serialize_user(user_doc))


async def login_user(payload: UserLoginRequest) -> TokenResponse:
    db = get_database()
    user = await db[COLLECTIONS["users"]].find_one({"email": payload.email.lower()})

    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated",
        )

    token = create_access_token({"sub": str(user["_id"]), "role": user["role"]})
    return TokenResponse(access_token=token, user=_serialize_user(user))


async def get_user_by_id(user_id: str) -> UserResponse:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    user = await get_database()[COLLECTIONS["users"]].find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return _serialize_user(user)


async def seed_admin_user(email: str, password: str, full_name: str) -> None:
    db = get_database()
    users = db[COLLECTIONS["users"]]

    existing = await users.find_one({"email": email.lower()})
    if existing:
        return

    now = datetime.now(timezone.utc)
    await users.insert_one(
        {
            "email": email.lower(),
            "password_hash": hash_password(password),
            "full_name": full_name,
            "role": ADMIN_ROLE,
            "is_active": True,
            "onboarding_completed": True,
            "created_at": now,
            "updated_at": now,
        }
    )
