from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models.transaction_model import Transaction
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from datetime import datetime


async def create_transaction(db: AsyncSession, transaction: TransactionCreate):
    db_transaction = Transaction(
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=Decimal(str(transaction.amount)),
        description=transaction.description,
        reference_transaction_id=transaction.reference_transaction_id,
        recipient_user_id=transaction.recipient_user_id
    )
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def get_transaction_by_id(db: AsyncSession, transaction_id: int):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()


async def get_all_transactions_of_a_user(
    db: AsyncSession, user_id: int, page: int = 1, page_limit: int = 10
):
    offset = (page - 1) * page_limit
    
    # Get total count
    count_query = select(func.count(Transaction.id)).filter(Transaction.user_id == user_id)
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Get transactions
    query = (
        select(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(page_limit)
    )
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    # Format response
    formatted_transactions = []
    for transaction in transactions:
        formatted_transactions.append({
            "transaction_id": transaction.id,
            "transaction_type": transaction.transaction_type,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "created_at": transaction.created_at
        })
    
    return {
        "transactions": formatted_transactions,
        "total": total,
        "page": page,
        "limit": page_limit
    }
