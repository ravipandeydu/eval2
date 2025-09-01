# Wallet Schema

from pydantic import BaseModel
from datetime import datetime


class WalletBase(BaseModel):
    user_id: int
    balance: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
