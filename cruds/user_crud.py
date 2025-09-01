# User CRUD
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: UserUpdate, user_id: int):
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


# Get Wallet Balance
async def get_wallet_balance(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user:
        return user.balance
    return None


# Add Money in Wallet
async def add_money_in_wallet(db: AsyncSession, user_id: int, amount: int):
    user = await get_user(db, user_id)
    if user:
        user.username = user.username
        user.email = user.email
        user.phone_number = user.phone_number
        user.password = user.password
        user.balance += amount
        user.updated_at = datetime.now()
        await db.commit()
        await db.refresh(user)
        return user
    return None


# Subtract Money from Wallet
async def subtract_money_from_wallet(db: AsyncSession, user_id: int, amount: int):
    user = await get_user(db, user_id)
    if user:
        user.username = user.username
        user.email = user.email
        user.phone_number = user.phone_number
        user.password = user.password
        user.balance -= amount
        await db.commit()
        await db.refresh(user)
        return user
    return None
