from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class User(BaseModel):
    id: int
    email: str
    is_active: bool
    insstmp: date
    updstmp: date


class UserResponse(BaseModel):
    id: int
    email: str


class LoginUser(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)


class RegisterUser(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)
