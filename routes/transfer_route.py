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


@transfer_router.get("/{transaction_id}")
async def get_transfer(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_transfer_by_id(db, transaction_id)
