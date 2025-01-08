from fastapi import HTTPException
from app.trainings.repositories import (
    get_user_trainings_from_db,
    create_training_in_db,
    add_training_exercise_in_db,
)
from app.trainings.models import (
    Training,
    TrainingResponse,
    AddTrainingExerciseRequest,
    TrainingExerciseResponse,
)


async def get_training_for_user(userid: int):
    trainings = await get_user_trainings_from_db(userid)
    return [Training(**t) for t in trainings]


async def create_new_training(userid: int, name: str):
    created = await create_training_in_db(userid, name)
    return Training(**created)


async def add_new_training_exercise(
    userid: int,
    trainingid: int,
    exerciseid: int,
    minsetnumber: int = None,
    maxsetnumber: int = None,
):
    # Trzeba sprawdzić, czy trening należy do użytkownika:
    # Oraz czy trainingid istnieje i czy należy do userid.

    # trainings = await get_user_trainings_from_db(userid)
    # if not any(t["id"] == trainingid for t in trainings):
    #     raise HTTPException(status_code=404, detail="Training plan not found or does not belong to this user.")

    new_exercise = await add_training_exercise_in_db(
        userid, trainingid, exerciseid, minsetnumber, maxsetnumber
    )
    return TrainingExerciseResponse(**new_exercise)
