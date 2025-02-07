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
    """
    Dane potrzebne do rozpoczęcia nowej sesji treningowej.
    Zakładamy, że user przekazuje trainingid (id planu treningu),
    start_time ustawimy w kodzie (np. "NOW()") lub pobierzemy od użytkownika.
    """

    trainingid: int


class EndTrainingSessionRequest(BaseModel):
    """
    Dane do zakończenia sesji – ewentualnie można przekazać end_time,
    ale często wystarczy ustawić to serwerowo na NOW().
    """

    end_time: Optional[datetime] = None
