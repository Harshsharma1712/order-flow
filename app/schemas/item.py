from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict

from .shop import ShopResponse


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0)
    is_available: Optional[bool] = True
    category: Optional[str] = None
    stock_quantity: int = Field(default=0, ge=0)


class ItemCreate(ItemBase):
    # shop_id: int
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0)
    category: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)


class ItemResponse(ItemBase):
    id: int
    shop_id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemWithShop(ItemResponse):
    shop: ShopResponse
