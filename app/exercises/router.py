from fastapi import APIRouter
from app.exercises.services import get_exercises

router = APIRouter()


# TODO get exercies by paries
@router.get("")
async def get_exercises_endpoint():
    return await get_exercises()
