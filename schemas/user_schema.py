from optparse import OptionParser
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phone_number: str
    balance: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    balance: Optional[int] = None


class UserInDB(UserBase):
    id: int
