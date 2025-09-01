from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.transaction_model import Transaction
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from datetime import datetime


async def create_transaction(db: AsyncSession, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.model_dump())
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


# get all transactions of a user with pagination with page limit 10
async def get_all_transactions_of_a_user(
    db: AsyncSession, user_id: int, page: int = 1, page_limit: int = 10
):
    offset = (page - 1) * page_limit
    query = (
        select(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.id.desc())
        .offset(offset)
        .limit(page_limit)
    )
    result = await db.execute(query)
    return result.scalars().all()
