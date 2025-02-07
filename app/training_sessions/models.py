from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TrainingSession(BaseModel):
    id: int
    userid: int
    trainingid: int
    start_time: datetime
    end_time: Optional[datetime] = None


class CreateTrainingSessionRequest(BaseModel):
    trainingid: int


class EndTrainingSessionRequest(BaseModel):
    end_time: Optional[datetime] = None
