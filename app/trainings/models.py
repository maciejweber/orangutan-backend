from pydantic import BaseModel
from typing import Optional, List


class Training(BaseModel):
    id: int
    userid: int
    name: str
    exercisesNumber: int = 0


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


class Exercise(BaseModel):
    id: int
    partiesid: int
    name: str
    image: Optional[bytes] = None
    hardrate: Optional[str] = None
    description: Optional[str] = None
    serieshint: Optional[int] = None
    counthint: Optional[int] = None
    breakhint: Optional[int] = None


class TrainingWithExercises(BaseModel):
    id: int
    userid: int
    name: str
    exercises: List[Exercise]
