from pydantic import BaseModel
from datetime import datetime


class Series(BaseModel):
    id: int
    userid: int
    exerciseid: int
    trainingid: int
    setnumber: int
    countnumber: int
    weight: float
    insstmp: datetime
    trainingsessionid: int


class CreateSeriesRequest(BaseModel):
    trainingsessionid: int
    trainingid: int
    exerciseid: int
    setnumber: int
    countnumber: int
    weight: float
