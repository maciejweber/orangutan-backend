from pydantic import BaseModel, field_validator
from typing import Optional, List

# from exercises.models import Exercise


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
    image: Optional[str]
    hardrate: Optional[str] = None
    description: Optional[str] = None
    serieshint: Optional[int] = None
    counthint: Optional[int] = None
    breakhint: Optional[int] = None
    position: str
    performing: str
    tips: str

    @field_validator("image")
    def build_image_url(cls, v):
        if v:
            return f"http://localhost:8000/images/{v}.jpg"
        return v


class TrainingWithExercises(BaseModel):
    id: int
    userid: int
    name: str
    exercises: List[Exercise]
