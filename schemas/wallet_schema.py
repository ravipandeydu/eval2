from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WalletBalanceResponse(BaseModel):
    user_id: int
    balance: float
    last_updated: datetime

    class Config:
        from_attributes = True


class AddMoneyRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = Field(default="Added money to wallet")


class WithdrawMoneyRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    description: Optional[str] = Field(default="Withdrew money from wallet")


class WalletTransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    amount: float
    new_balance: float
    transaction_type: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
