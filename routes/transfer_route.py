# Transfer Route
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.transfer_crud as crud
from models.transaction_model import Transaction
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from datetime import datetime
from db.database import get_db

transfer_router = APIRouter(
    prefix="/transfer",
    tags=["transfer"],
)


@transfer_router.post("/")
async def create_transfer(
    sender_user_id: int,
    recipient_user_id: int,
    amount: int,
    description: str,
    db: AsyncSession = Depends(get_db),
):
    return await crud.transfer_money(
        db, sender_user_id, recipient_user_id, amount, description
    )
