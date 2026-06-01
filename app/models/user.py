from pydantic import BaseModel, EmailStr
from typing import Optional


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
