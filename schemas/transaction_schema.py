from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TransactionBase(BaseModel):
    user_id: int
    transaction_type: str = Field(..., pattern="^(CREDIT|DEBIT|TRANSFER_IN|TRANSFER_OUT)$")
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = None
    reference_transaction_id: Optional[int] = None
    recipient_user_id: Optional[int] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    user_id: Optional[int] = None
    transaction_type: Optional[str] = Field(None, pattern="^(CREDIT|DEBIT|TRANSFER_IN|TRANSFER_OUT)$")
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    reference_transaction_id: Optional[int] = None
    recipient_user_id: Optional[int] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
