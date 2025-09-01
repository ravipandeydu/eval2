from datetime import datetime
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from models.user_model import User
from models.transaction_model import Transaction
from schemas.user_schema import UserCreate, UserUpdate
from schemas.transaction_schema import TransactionCreate
import cruds.transaction_crud as transaction_crud


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):
    # Check if username or email already exists
    existing_user = await db.execute(
        select(User).filter(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        balance=Decimal('0.00'),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: UserUpdate, user_id: int):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_user, key, value)
    
    db_user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_wallet_balance(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if user:
        return {
            "user_id": user.id,
            "balance": float(user.balance),
            "last_updated": user.updated_at,
        }
    return None


async def add_money_in_wallet(db: AsyncSession, user_id: int, amount: float, description: str = "Added money to wallet"):
    user = await get_user(db, user_id)
    if not user:
        return None
    
    # Create CREDIT transaction
    transaction_data = TransactionCreate(
        user_id=user_id,
        transaction_type="CREDIT",
        amount=amount,
        description=description
    )
    transaction = await transaction_crud.create_transaction(db, transaction_data)
    
    # Update user balance
    user.balance += Decimal(str(amount))
    user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    
    return {
        "transaction_id": transaction.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": float(user.balance),
        "transaction_type": "CREDIT",
        "description": description,
        "created_at": transaction.created_at
    }


async def subtract_money_from_wallet(db: AsyncSession, user_id: int, amount: float, description: str = "Withdrew money from wallet"):
    user = await get_user(db, user_id)
    if not user:
        return None
    
    # Check sufficient balance
    if float(user.balance) < amount:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Insufficient balance",
                "current_balance": float(user.balance),
                "required_amount": amount
            }
        )
    
    # Create DEBIT transaction
    transaction_data = TransactionCreate(
        user_id=user_id,
        transaction_type="DEBIT",
        amount=amount,
        description=description
    )
    transaction = await transaction_crud.create_transaction(db, transaction_data)
    
    # Update user balance
    user.balance -= Decimal(str(amount))
    user.updated_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    
    return {
        "transaction_id": transaction.id,
        "user_id": user.id,
        "amount": amount,
        "new_balance": float(user.balance),
        "transaction_type": "DEBIT",
        "description": description,
        "created_at": transaction.created_at
    }
