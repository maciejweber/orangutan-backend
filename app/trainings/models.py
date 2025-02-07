from pydantic import BaseModel
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
    image: Optional[str] = (
        "https://www.fabrykasily.pl/upload/gallery/2018/07/id_18973_1532436684_1260x841.jpg"
    )
    hardrate: Optional[str] = None
    description: Optional[str] = None
    serieshint: Optional[int] = None
    counthint: Optional[int] = None
    breakhint: Optional[int] = None
    position: str = "Połóż się na ławce, stopy stabilnie na ziemi, plecy lekko wygięte."
    performing: str = (
        "Chwyć sztangę na szerokość barków, opuść ją powoli do klatki piersiowej, a następnie dynamicznie wypchnij do góry."
    )
    tips: str = (
        "Nie blokuj łokci na górze, kontroluj ruch, nie odbijaj sztangi od klatki."
    )


class TrainingWithExercises(BaseModel):
    id: int
    userid: int
    name: str
    exercises: List[Exercise]
