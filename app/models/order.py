from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime,ForeignKey, Numeric, Enum, Index

from sqlalchemy.orm import relationship

from .base import Base
from .enums import ItemStatus


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)

    total_amount = Column(Numeric(10, 2), nullable=False)

    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.PENDING)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # relationships
    user = relationship("User", back_populates="orders")

    shop = relationship("Shop", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_shop_status', 'shop_id', 'status'),
        Index('idx_created_at', 'created_at'),
    )

