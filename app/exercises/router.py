from fastapi import APIRouter
from app.exercises.services import get_exercises

router = APIRouter()


@router.get("/exercises")
async def get_exercises_endpoint():
    return await get_exercises()
