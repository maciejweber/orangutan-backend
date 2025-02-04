from fastapi import APIRouter
from app.exercises.services import get_exercises
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_current_user
from app.users.models import User


router = APIRouter()


# TODO get exercies by paries
@router.get("")
async def get_exercises_endpoint(current_user: User = Depends(get_current_user)):
    return await get_exercises()
