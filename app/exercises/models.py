from pydantic import BaseModel
from typing import Optional


class Exercise(BaseModel):
    id: int
    partiesid: int
    name: str
    image: Optional[bytes]
    hardrate: Optional[str]
    description: Optional[str]
    serieshint: Optional[str]
    counthint: Optional[str]
    breakhint: Optional[str]
