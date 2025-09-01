# User Routes
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.user_crud as crud
from db.database import get_db

wallet_router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@wallet_router.get("/{user_id}/balance")
async def get_wallet_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_wallet_balance(db, user_id)


@wallet_router.post("/{user_id}/add-money")
async def add_money_in_wallet(
    user_id: int, amount: int, db: AsyncSession = Depends(get_db)
):
    return await crud.add_money_in_wallet(db, user_id, amount)


@wallet_router.post("/{user_id}/withdraw-money")
async def withdraw_money_from_wallet(
    user_id: int, amount: int, db: AsyncSession = Depends(get_db)
):
    return await crud.subtract_money_from_wallet(db, user_id, amount)
