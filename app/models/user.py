from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Index
from sqlalchemy.orm import relationship

from .base import Base
from .enums import UserType


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)

    username = Column(String(255), unique=True, nullable=False, index=True)

    hashed_password = Column(String(255), nullable=False)

    full_name = Column(String(255))

    user_type = Column(Enum(UserType), nullable=False, default=UserType.NORMAL)

    is_active = Column(Boolean, default=True)

    phone = Column(String(20))

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # RealtionShips
    owned_shops = relationship("Shop", back_populates="owner", cascade="all, delete-orphan")

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_type_active', 'user_type', 'is_active'),
    )

