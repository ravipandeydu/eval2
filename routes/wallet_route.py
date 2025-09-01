from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.user_crud as crud
from schemas.wallet_schema import (
    WalletBalanceResponse,
    AddMoneyRequest,
    WithdrawMoneyRequest,
    WalletTransactionResponse
)
from db.database import get_db

wallet_router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@wallet_router.get("/{user_id}/balance", response_model=WalletBalanceResponse)
async def get_wallet_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_wallet_balance(db, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@wallet_router.post("/{user_id}/add-money", response_model=WalletTransactionResponse, status_code=201)
async def add_money_in_wallet(
    user_id: int, 
    request: AddMoneyRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await crud.add_money_in_wallet(db, user_id, request.amount, request.description)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@wallet_router.post("/{user_id}/withdraw", response_model=WalletTransactionResponse, status_code=201)
async def withdraw_money_from_wallet(
    user_id: int, 
    request: WithdrawMoneyRequest, 
    db: AsyncSession = Depends(get_db)
):
    result = await crud.subtract_money_from_wallet(db, user_id, request.amount, request.description)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result
