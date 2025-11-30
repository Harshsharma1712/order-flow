from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric, Text, Index

from sqlalchemy.orm import relationship

from .base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False, index=True)

    description = Column(Text)

    price = Column(Numeric(10, 2), nullable=False)

    is_available = Column(Boolean, default=True)

    stock_quantity = Column(Integer, default=0)

    category = Column(String(100), index=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # realtionships
    shop = relationship("Shop",  back_populates="items")

    order_items = relationship("OrderItem", back_populates="item")

    __table_args__ = (
        Index('idx_shop_available', 'shop_id', 'is_available'),
        Index('idx_shop_category', 'shop_id', 'category'),
    )

