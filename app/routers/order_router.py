from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.item import Item
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderDetailResponse
from app.auth.dependencies import get_current_user


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create", response_model=OrderDetailResponse)
async def create_order(
    data: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Fetch All Items in Order
    item_ids = [i.item_id for i in data.items]

    query = (
        select(Item)
        .where(
            Item.id.in_(item_ids),
            Item.shop_id == data.shop_id
        )
    )

    result = await db.execute(query)

    items = result.scalars().all()

    # Validate items exist & belong to shop
    if len(items) != len(item_ids):
        raise HTTPException(
            status_code=400,
            detail="Some items are invalid or do not belong to the selected shop"
        )
    
    # Create a map for quick access
    item_map = {item.id: item for item in items}


    # 2. Calculate Total Amount
    total_amount = Decimal("0.00")
    order_items_data = []

    for input_item in data.items:
        db_item = item_map[input_item.item_id]

        unit_price = db_item.price
        subtotal = unit_price * input_item.quantity

        total_amount += subtotal

        order_items_data.append({
            "item_id": db_item.id,
            "quantity": input_item.quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,
            "notes": input_item.notes
        })

    # 3. Create Order

    order = Order(
        user_id = current_user.id,
        shop_id = data.shop_id,
        delivery_address = data.delivery_address,
        notes = data.notes,
        total_amount = total_amount
    )

    db.add(order)

    await db.flush()     # we get order.id here

    # 4. Create Order Items
    for oi in order_items_data:
        db.add(OrderItem(order_id=order.id, **oi))

    # Save everything
    await db.commit()

    query = (
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.user),
            selectinload(Order.shop),
            selectinload(Order.order_items).selectinload(OrderItem.item)
        )
    )

    result = await db.execute(query)
    full_order = result.scalars().first()

    return full_order




