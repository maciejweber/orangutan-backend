from fastapi import HTTPException
from app.trainings.repositories import (
    get_user_trainings_from_db,
    create_training_in_db,
    add_training_exercise_in_db,
    get_training_exercises_from_db,
    delete_training_exercise_from_db,
    delete_all_exercises_for_training_from_db,
    delete_training_from_db,
)
from app.trainings.models import (
    Training,
    TrainingResponse,
    AddTrainingExerciseRequest,
    TrainingWithExercises,
    TrainingExerciseResponse,
)
from app.trainings.models import Exercise


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
    # minsetnumber: int = None,
    # maxsetnumber: int = None,
):
    # Trzeba sprawdzić, czy trening należy do użytkownika:
    # Oraz czy trainingid istnieje i czy należy do userid.

    trainings = await get_user_trainings_from_db(userid)
    if not any(t["id"] == trainingid for t in trainings):
        raise HTTPException(
            status_code=404,
            detail="Training plan not found or does not belong to this user.",
        )

    new_exercise = await add_training_exercise_in_db(
        userid,
        trainingid,
        exerciseid,
        #   minsetnumber
        # , maxsetnumber
    )
    return TrainingExerciseResponse(**new_exercise)


async def delete_training_exercise(userid: int, trainingid: int, exerciseid: int):
    trainings = await get_user_trainings_from_db(userid)
    if not any(t["id"] == trainingid for t in trainings):
        raise HTTPException(
            status_code=404,
            detail="Training plan not found or does not belong to this user.",
        )

    deleted = await delete_training_exercise_from_db(userid, trainingid, exerciseid)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found in training or already removed.",
        )

    return deleted


async def get_training_with_exercises(userid: int, trainingid: int):

    trainings = await get_user_trainings_from_db(userid)
    training = next((t for t in trainings if t["id"] == trainingid), None)
    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training plan not found or does not belong to this user.",
        )

    exercises = await get_training_exercises_from_db(trainingid)
    exercises_list = [Exercise(**ex) for ex in exercises]

    training_with_exercises = TrainingWithExercises(
        id=training["id"],
        userid=training["userid"],
        name=training["name"],
        exercises=exercises_list,
    )

    return training_with_exercises


async def delete_training(userid: int, trainingid: int):
    # 1. Sprawdź, czy trening należy do użytkownika
    trainings = await get_user_trainings_from_db(userid)
    if not any(t["id"] == trainingid for t in trainings):
        raise HTTPException(
            status_code=404,
            detail="Training plan not found or does not belong to this user.",
        )

    # 2. (Opcjonalnie) Usuń ćwiczenia powiązane z trainingid,
    #    jeśli nie mamy w bazie CASCADE:
    await delete_all_exercises_for_training_from_db(trainingid)

    # 3. Usuń sam trening:
    deleted_training = await delete_training_from_db(userid, trainingid)
    if not deleted_training:
        raise HTTPException(
            status_code=404, detail="Training not found or already removed."
        )
    return deleted_training
