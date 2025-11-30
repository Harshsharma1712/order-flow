from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime,ForeignKey, Numeric, Index

from sqlalchemy.orm import relationship

from .base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)

    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False)

    quantity = Column(Integer, nullable=False, default=1)

    unit_price = Column(Numeric(10, 2), nullable=False)

    subtotal = Column(Numeric(10, 2), nullable=False)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    # relationships
    order = relationship("Order", back_populates="order_items")

    item = relationship("Item", back_populates="order_items")

    __table_args__ = (
        Index('idx_order_item', 'order_id', 'item_id'),
    )

