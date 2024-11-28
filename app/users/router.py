
from fastapi import APIRouter, Depends
import asyncpg
from app.database import DataBasePool
from app.users.services import get_users

users = APIRouter()

@users.get("/users")
async def get_users_endpoint(db_pool: asyncpg.Pool = Depends(DataBasePool.get_pool)):
    users = await get_users(db_pool)
    return users