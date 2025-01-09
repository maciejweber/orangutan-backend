from fastapi import APIRouter, Depends
from app.series.services import create_new_series
from app.series.models import CreateSeriesRequest, Series
from app.dependencies.auth import get_current_user
from app.users.models import User

router = APIRouter()


@router.post("", response_model=Series)
async def add_series_endpoint(
    request: CreateSeriesRequest,
    current_user: User = Depends(get_current_user),
):
    series = await create_new_series(
        userid=current_user.id,
        trainingid=request.trainingid,
        exerciseid=request.exerciseid,
        setnumber=request.setnumber,
        countnumber=request.countnumber,
        weight=request.weight,
    )
    return series
