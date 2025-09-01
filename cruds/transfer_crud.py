from decimal import Decimal
from datetime import datetime
import uuid
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import cruds.transaction_crud as transaction_crud
from models.transaction_model import Transaction
from models.user_model import User
from schemas.transaction_schema import TransactionCreate


async def transfer_money(
    db: AsyncSession,
    sender_user_id: int,
    recipient_user_id: int,
    amount: float,
    description: str = "Money transfer",
):
    # Validate users exist
    sender_query = select(User).filter(User.id == sender_user_id)
    sender_result = await db.execute(sender_query)
    sender = sender_result.scalars().first()
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    
    recipient_query = select(User).filter(User.id == recipient_user_id)
    recipient_result = await db.execute(recipient_query)
    recipient = recipient_result.scalars().first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    # Check if sender and recipient are different
    if sender_user_id == recipient_user_id:
        raise HTTPException(status_code=400, detail="Cannot transfer to yourself")
    
    # Check sufficient balance
    if float(sender.balance) < amount:
        raise HTTPException(
            status_code=400, 
            detail={
                "error": "Insufficient balance",
                "current_balance": float(sender.balance),
                "required_amount": amount
            }
        )
    
    # Generate unique transfer ID
    transfer_id = str(uuid.uuid4())
    
    try:
        # Create TRANSFER_OUT transaction for sender
        sender_transaction = TransactionCreate(
            user_id=sender_user_id,
            transaction_type="TRANSFER_OUT",
            amount=amount,
            description=description,
            recipient_user_id=recipient_user_id
        )
        sender_tx = await transaction_crud.create_transaction(db, sender_transaction)
        
        # Create TRANSFER_IN transaction for recipient
        recipient_transaction = TransactionCreate(
            user_id=recipient_user_id,
            transaction_type="TRANSFER_IN",
            amount=amount,
            description=description,
            reference_transaction_id=sender_tx.id
        )
        recipient_tx = await transaction_crud.create_transaction(db, recipient_transaction)
        
        # Link the transactions
        sender_tx.reference_transaction_id = recipient_tx.id
        
        # Update balances atomically
        sender.balance -= Decimal(str(amount))
        recipient.balance += Decimal(str(amount))
        sender.updated_at = datetime.now()
        recipient.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(sender)
        await db.refresh(recipient)
        
        return {
            "transfer_id": transfer_id,
            "sender_transaction_id": sender_tx.id,
            "recipient_transaction_id": recipient_tx.id,
            "amount": amount,
            "sender_new_balance": float(sender.balance),
            "recipient_new_balance": float(recipient.balance),
            "status": "completed",
            "created_at": sender_tx.created_at
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Transfer failed")


async def get_transfer_by_id(
    db: AsyncSession,
    transfer_id: str,
):
    # For simplicity, we'll use the transaction ID as transfer ID
    # In a real system, you'd have a separate transfers table
    try:
        transaction_id = int(transfer_id)
        query = select(Transaction).filter(Transaction.id == transaction_id)
        result = await db.execute(query)
        transaction = result.scalars().first()
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transfer not found")
        
        return {
            "transfer_id": str(transaction.id),
            "sender_user_id": transaction.user_id if transaction.transaction_type == "TRANSFER_OUT" else transaction.recipient_user_id,
            "recipient_user_id": transaction.recipient_user_id if transaction.transaction_type == "TRANSFER_OUT" else transaction.user_id,
            "amount": float(transaction.amount),
            "description": transaction.description,
            "status": "completed",
            "created_at": transaction.created_at
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid transfer ID")


async def get_transfer_by_transaction_id(
    db: AsyncSession,
    transaction_id: int,
):
    query = select(Transaction).filter(Transaction.id == transaction_id)
    result = await db.execute(query)
    return result.scalars().first()
