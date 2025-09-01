from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.user_crud as crud
import cruds.transaction_crud as transaction_crud
from schemas.user_schema import UserCreate, UserUpdate
from db.database import get_db

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@user_router.get("/{user_id}")
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user(db, user_id)


@user_router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db, user)


@user_router.put("/{user_id}")
async def update_user(
    user: UserUpdate, user_id: int, db: AsyncSession = Depends(get_db)
):
    return await crud.update_user(db, user, user_id)


@user_router.get("/{user_id}/balance")
async def get_wallet_balance(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_wallet_balance(db, user_id)


@user_router.get("/{user_id}/transactions")
async def get_user_transactions(
    user_id: int,
    page: int = 1,
    page_limit: int = 10,
    db: AsyncSession = Depends(get_db),
):
    return await transaction_crud.get_all_transactions_of_a_user(
        db, user_id, page, page_limit
    )
