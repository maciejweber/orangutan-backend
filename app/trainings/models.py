from pydantic import BaseModel
from typing import Optional


class Training(BaseModel):
    id: int
    userid: int
    name: str


class CreateTrainingRequest(BaseModel):
    name: str


class TrainingResponse(BaseModel):
    id: int
    userid: int
    name: str


class AddTrainingExerciseRequest(BaseModel):
    exerciseid: int
    # minsetnumber: Optional[int] = None
    # maxsetnumber: Optional[int] = None


class TrainingExerciseResponse(BaseModel):
    id: int
    userid: int
    trainingid: int
    exerciseid: int
    # minsetnumber: Optional[int]
    # maxsetnumber: Optional[int]
