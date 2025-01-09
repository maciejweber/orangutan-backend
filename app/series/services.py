from fastapi import HTTPException
from app.series.repositories import (
    add_series_in_db,
    get_training_by_id,
    get_exercise_in_training,
)
from app.series.models import Series, CreateSeriesRequest


async def create_new_series(
    userid: int,
    trainingid: int,
    exerciseid: int,
    setnumber: int,
    countnumber: int,
    weight: float,
):
    training = await get_training_by_id(userid, trainingid)
    if not training:
        raise HTTPException(
            status_code=404,
            detail="Training plan not found or does not belong to this user.",
        )

    exercise = await get_exercise_in_training(userid, trainingid, exerciseid)
    if not exercise:
        raise HTTPException(
            status_code=404,
            detail="Exercise not found in the specified training.",
        )

    new_series = await add_series_in_db(
        userid, trainingid, exerciseid, setnumber, countnumber, weight
    )
    return Series(**new_series)
