# Transaction Schema
from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    user_id: int
    transaction_type: str
    amount: int
    description: str = None
    # reference_transaction_id: int = None
    # recipient_user_id: int = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    user_id: Optional[int] = None
    transaction_type: Optional[str] = None
    amount: Optional[int] = None
    description: Optional[str] = None
    # reference_transaction_id: Optional[int] = None
    # recipient_user_id: Optional[int] = None


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
