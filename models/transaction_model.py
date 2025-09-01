from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(255))
    # reference_transaction_id = Column(Integer, ForeignKey("transactions.id"))
    # recipient_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="transactions")
    # reference_transaction = relationship(
    #     "Transaction", back_populates="transactions", remote_side=[id]
    # )
    # recipient_user = relationship(
    #     "User", back_populates="transactions", foreign_keys=[recipient_user_id]
    # )
