from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from cruds import transfer_crud
from db.database import get_db
from schemas.transfer_schema import (
    TransferRequest,
    TransferResponse,
    TransferDetailResponse,
    InsufficientBalanceError
)

router = APIRouter()


@router.post("/transfer/", response_model=TransferResponse)
async def create_transfer(
    transfer_request: TransferRequest,
    db: AsyncSession = Depends(get_db),
):
    """Transfer money between users"""
    try:
        result = await transfer_crud.transfer_money(
            db=db,
            sender_user_id=transfer_request.sender_user_id,
            recipient_user_id=transfer_request.recipient_user_id,
            amount=transfer_request.amount,
            description=transfer_request.description
        )
        return TransferResponse(**result)
    except HTTPException as e:
        if e.status_code == 400 and isinstance(e.detail, dict) and "error" in e.detail:
            # Handle insufficient balance error
            raise HTTPException(
                status_code=400,
                detail=InsufficientBalanceError(
                    error=e.detail["error"],
                    current_balance=e.detail["current_balance"],
                    required_amount=e.detail["required_amount"]
                ).dict()
            )
        raise e


@router.get("/transfer/{transfer_id}", response_model=TransferDetailResponse)
async def get_transfer(
    transfer_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get transfer details by transfer ID"""
    transfer = await transfer_crud.get_transfer_by_id(db, transfer_id)
    return TransferDetailResponse(**transfer)
