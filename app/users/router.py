from fastapi import APIRouter, Depends, HTTPException
import asyncpg
from app.database import DataBasePool
from app.users.services import get_users, authenticate_user
from app.users.models import UserLogin


users = APIRouter()


@users.get("/users")
async def get_users_endpoint(db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    users = await get_users(db_pool)
    return users


@users.post("/login")
async def login_endpoint(login_request: UserLogin, db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    user = await authenticate_user(db_pool, login_request.email, login_request.passwd)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user
