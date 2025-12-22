from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime,ForeignKey, Numeric, Enum, Index, Text

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

    delivery_address = Column(Text, nullable=True)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # for order cancelation 
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    cancel_reason = Column(Text, nullable=True)


    # relationships
    user = relationship("User", back_populates="orders")

    shop = relationship("Shop", back_populates="orders")

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_shop_status', 'shop_id', 'status'),
        Index('idx_created_at', 'created_at'),
    )

