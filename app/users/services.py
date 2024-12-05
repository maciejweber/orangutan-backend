from app.users.repositories import (
    get_users_from_db,
    get_user_details_from_db_by_id,
    get_user_details_from_db_by_email,
)
from app.users.models import User
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
    print(user)
    if not user:
        return HTTPException(status_code=404, detail="Invalid email or password")

    # Odhashuj hasło - bcrypt
    # Czy hasło jest poprawne?
    # Utwórz token JWT
    # Zwróc token JWT bez danych uzytkownika

    return User(**user)
