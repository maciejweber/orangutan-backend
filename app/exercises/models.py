from pydantic import BaseModel, field_validator
from typing import Optional


class Exercise(BaseModel):
    id: int
    partiesid: int
    name: str
    image: Optional[str]
    hardrate: Optional[str]
    description: Optional[str]
    serieshint: Optional[int]
    counthint: Optional[int]
    breakhint: Optional[int]
    position: str
    performing: str
    tips: str

    @field_validator("image")
    def build_image_url(cls, v):
        if v:
            return f"http://localhost:8000/images/{v}.jpg"
        return v
