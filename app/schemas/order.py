from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from .enums import ItemStatusEnum
from .user import UserResponse
from .shop import ShopResponse
from .item import ItemResponse


# ========== Order Item Schemas ==========

class OrderItemBase(BaseModel):
    item_id: int
    quantity: int = Field(..., gt=0)
    notes: Optional[str] = None


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    item_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    notes: Optional[str] = None
    created_at: datetime
    item: ItemResponse

    model_config = ConfigDict(from_attributes=True)


# ========== Order Schemas ==========

class OrderBase(BaseModel):
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    shop_id: int
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderUpdate(BaseModel):
    delivery_address: Optional[str] = None
    notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: ItemStatusEnum


class OrderResponse(OrderBase):
    id: int
    user_id: int
    shop_id: int
    total_amount: Decimal
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderDetailResponse(OrderResponse):
    user: UserResponse
    shop: ShopResponse
    order_items: List[OrderItemResponse]
