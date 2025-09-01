from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.transaction_crud as transaction_crud
from models.transaction_model import Transaction
from models.user_model import User
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from datetime import datetime


async def transfer_money(
    db: AsyncSession,
    sender_user_id: int,
    recipient_user_id: int,
    amount: int,
    description: str = None,
):
    query = select(User).filter(User.id == sender_user_id)
    result = await db.execute(query)
    sender = result.scalars().first()
    if sender.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    query = select(User).filter(User.id == recipient_user_id)
    result = await db.execute(query)
    recipient = result.scalars().first()
    if not recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")

    recipient_transaction = TransactionCreate(
        user_id=sender_user_id,
        transaction_type="debit",
        amount=amount,
        description=description,
    )
    recipient_transaction = await transaction_crud.create_transaction(
        db, recipient_transaction
    )

    sender_transaction = TransactionCreate(
        user_id=recipient_user_id,
        transaction_type="credit",
        amount=amount,
        description=description,
    )
    sender_transaction = await transaction_crud.create_transaction(
        db, sender_transaction
    )

    sender.balance -= amount
    recipient.balance += amount
    await db.commit()

    return {
        "sender": sender,
        "recipient_user_id": recipient_user_id,
        "amount": amount,
        "description": description,
    }


async def get_transfer_by_id(
    db: AsyncSession,
    transfer_id: int,
):
    query = select(Transaction).filter(Transaction.id == transfer_id)
    result = await db.execute(query)
    return result.scalars().first()
