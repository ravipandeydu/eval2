from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TransferRequest(BaseModel):
    sender_user_id: int
    recipient_user_id: int
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = Field(default="Money transfer")


class TransferResponse(BaseModel):
    transfer_id: str
    sender_transaction_id: int
    recipient_transaction_id: int
    amount: float
    sender_new_balance: float
    recipient_new_balance: float
    status: str = "completed"
    created_at: datetime

    class Config:
        from_attributes = True


class TransferDetailResponse(BaseModel):
    transfer_id: str
    sender_user_id: int
    recipient_user_id: int
    amount: float
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class InsufficientBalanceError(BaseModel):
    error: str = "Insufficient balance"
    current_balance: float
    required_amount: float