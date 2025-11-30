from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Index
from sqlalchemy.orm import relationship

from .base import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False, index=True)

    description = Column(Text)

    address = Column(String(255))

    phone = Column(String(20))

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relationships
    owner = relationship("User", back_populates="owned_shops")

    items = relationship("Item", back_populates="shop", cascade="all, delete-orphan")

    orders = relationship("Order", back_populates="shop", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_owner_active', 'owner_id', 'is_active'),
    )

