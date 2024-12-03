from fastapi import APIRouter
from app.users.services import get_users

router = APIRouter()


@router.get("/")
async def get_users_endpoint():
    users = await get_users()
    return users
