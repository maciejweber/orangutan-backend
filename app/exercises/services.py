from app.exercises.repositories import get_all_exercises_from_db
from app.exercises.models import Exercise


async def get_exercises():
    exercises = await get_all_exercises_from_db()
    return [Exercise(**ex) for ex in exercises]
