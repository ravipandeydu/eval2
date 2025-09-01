from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # 'CREDIT', 'DEBIT', 'TRANSFER_IN', 'TRANSFER_OUT'
    amount = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(255))
    reference_transaction_id = Column(Integer, ForeignKey("transactions.id"))  # For linking transfer transactions
    recipient_user_id = Column(Integer, ForeignKey("users.id"))  # For transfers
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions", foreign_keys=[user_id])
