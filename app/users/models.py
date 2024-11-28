from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class User(BaseModel):
    id: int
    email: str
    is_active: bool
    insstmp: date
    updstmp: date


class UserCreate(BaseModel):
    email: str
    passwd: str = Field(max_length=100, min_length=8)
    is_active: bool


class UserUpdate(BaseModel):
    email: Optional[str]
    passwd: Optional[str]
    is_active: Optional[bool]
    updstmp: Optional[date]

