# User Model
from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_number = Column(String(15))
    balance = Column(DECIMAL(10, 2), default=0.00)
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now(), onupdate=datetime.now)

    transactions = relationship("Transaction", back_populates="user", foreign_keys="Transaction.user_id")
