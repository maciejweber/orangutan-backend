from fastapi import APIRouter, Depends
from app.trainings.services import (
    get_training_for_user,
    create_new_training,
    add_new_training_exercise,
    get_training_with_exercises,
)
from app.trainings.models import (
    CreateTrainingRequest,
    AddTrainingExerciseRequest,
    TrainingWithExercises,
)
from app.dependencies.auth import get_current_user
from app.users.models import User

router = APIRouter()


@router.get("")
async def get_user_trainings_endpoint(current_user: User = Depends(get_current_user)):
    return await get_training_for_user(current_user.id)


@router.post("")
async def create_training_endpoint(
    request: CreateTrainingRequest, current_user: User = Depends(get_current_user)
):
    new_training = await create_new_training(current_user.id, request.name)
    return new_training


@router.post("/{training_id}/exercises")
async def add_training_exercise_endpoint(
    training_id: int,
    request: AddTrainingExerciseRequest,
    current_user: User = Depends(get_current_user),
):
    exercise = await add_new_training_exercise(
        current_user.id,
        training_id,
        request.exerciseid,
        # request.minsetnumber,
        # request.maxsetnumber,
    )
    return exercise


@router.get("/{training_id}", response_model=TrainingWithExercises)
async def get_training_with_exercises_endpoint(
    training_id: int,
    current_user: User = Depends(get_current_user),
):
    training = await get_training_with_exercises(current_user.id, training_id)
    return training
