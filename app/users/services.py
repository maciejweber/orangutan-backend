import bcrypt

from app.users.repositories import (
    get_users_from_db,
    get_user_details_from_db_by_id,
    get_user_details_from_db_by_email,
    create_user_in_db,
)
from app.users.models import UserResponse, User
from app.utils.jwt import create_jwt_token
from fastapi import HTTPException


async def get_users():
    users = await get_users_from_db()
    print(users)
    return [User(**dict(user)) for user in users]


async def get_user_details(id: int):
    user = await get_user_details_from_db_by_id(id)
    if not user:
        return HTTPException(status_code=404, detail="User not found")
    return User(**user)


async def login_user(email: str, password: str):
    user = await get_user_details_from_db_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid email or password")

    # if not bcrypt.checkpw(password.encode(), user["hashed_password"].encode()):
    #     raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_jwt_token({"sub": user["email"], "user_id": user["id"]})

    return {"access_token": access_token}


async def register_user(email: str, password: str):
    existing_user = await get_user_details_from_db_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    created_user = await create_user_in_db(email, password)

    return UserResponse(**created_user)
