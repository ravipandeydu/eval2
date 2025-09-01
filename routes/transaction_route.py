from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from cruds import transaction_crud
from db.database import get_db
from schemas.transaction_schema import (
    TransactionCreate,
    TransactionResponse,
    Transaction
)
from typing import List

router = APIRouter()


@router.post("/transactions/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new transaction"""
    try:
        result = await transaction_crud.create_transaction(db, transaction)
        return TransactionResponse(
            transaction_id=result.id,
            user_id=result.user_id,
            transaction_type=result.transaction_type,
            amount=float(result.amount),
            description=result.description,
            created_at=result.created_at,
            reference_transaction_id=result.reference_transaction_id,
            recipient_user_id=result.recipient_user_id
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/transactions/detail/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_detail(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get transaction details by transaction ID"""
    transaction = await transaction_crud.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return TransactionResponse(
        transaction_id=transaction.id,
        user_id=transaction.user_id,
        transaction_type=transaction.transaction_type,
        amount=float(transaction.amount),
        description=transaction.description,
        created_at=transaction.created_at,
        reference_transaction_id=transaction.reference_transaction_id,
        recipient_user_id=transaction.recipient_user_id
    )


@router.get("/transactions/", response_model=dict)
async def get_transactions(
    user_id: int = Query(..., description="User ID to get transactions for"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of transactions per page"),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated transactions for a user"""
    try:
        result = await transaction_crud.get_all_transactions_of_a_user(
            db, user_id, page, limit
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))