from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from decimal import Decimal

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.item import Item
from app.models.shop import Shop
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderDetailResponse
from app.schemas.order import OrderStatusUpdate
from app.auth.dependencies import get_current_user
from app.utils.resend_email_service import send_order_ready_email, send_order_picked_email


router = APIRouter(prefix="/orders", tags=["Orders"])

# POST Create Order by user
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


# GET Shop Orders (Shop Owner Only)
@router.get("/shop/{shop_id}", response_model=list[OrderDetailResponse])
async def get_shop_orders(
    shop_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # check if shop belongs to current owner
    result = await db.execute(
        select(Shop).where(Shop.id == shop_id, Shop.owner_id == current_user.id)
    )

    shop = result.scalars().first()

    if not shop:
        raise HTTPException(
            status_code=403,
            detail= "You are not the owner of this shop"
        )
    
    query = (
        select(Order)
        .where(Order.shop_id == shop_id)
        .options(
            selectinload(Order.user),
            selectinload(Order.shop),
            selectinload(Order.order_items).selectinload(OrderItem.item)
        )
        .order_by(Order.created_at.desc())
    )

    result = await db.execute(query)

    return result.scalars().unique().all()


# Update Order Status (Shop Owner Only) and send email when status is ready
@router.patch("/{order_id}/status", response_model=OrderDetailResponse)
async def update_order_status(
    order_id: int,
    data: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Fetch order with shop relation
    query = (
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.shop))
    )
    result = await db.execute(query)

    order = result.scalars().first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail= "Order not found"
        )
    
    # 2. Check owner permissions
    if order.shop.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail= "You are not the owner of this shop"
        )
    
    # 3. Update status
    order.status = data.status

    await db.commit()

    # SEND EMAIL IF STATUS = READY
    if data.status.value.lower() == "ready":
        # Fetch full order details for email
        email_query = (
            select(Order)
            .where(Order.id == order.id)
            .options(
                selectinload(Order.user),
                selectinload(Order.shop),
                selectinload(Order.order_items).selectinload(OrderItem.item)
            )
        )

        email_result = await db.execute(email_query)
        order_full = email_result.scalars().first()

        # Prepare email data
        email_payload = {
            "id": order_full.id,
            "shop_name": order_full.shop.name,
            "total_amount": str(order_full.total_amount),
            "delivery_address": order_full.delivery_address,
            "items": [
                {
                    "name": oi.item.name,
                    "quantity": oi.quantity,
                    "subtotal": str(oi.subtotal)
                }
                for oi in order_full.order_items
            ]
        }

        # Send email to user
        await send_order_ready_email(
            to_email=order_full.user.email,
            order=email_payload
        )
    

    # SEND EMAIL IF STATUS = PICKED
    if data.status.value.lower() == "picked":
        # Fetch full order details for email
        email_query = (
            select(Order)
            .where(Order.id == order.id)
            .options(
                selectinload(Order.user),
                selectinload(Order.shop),
                selectinload(Order.order_items).selectinload(OrderItem.item)
            )
        )

        email_result = await db.execute(email_query)
        order_full = email_result.scalars().first()

        # Prepare email data
        email_payload = {
            "id": order_full.id,
            "shop_name": order_full.shop.name,
            "total_amount": str(order_full.total_amount),
            "delivery_address": order_full.delivery_address,
            "items": [
                {
                    "name": oi.item.name,
                    "quantity": oi.quantity,
                    "subtotal": str(oi.subtotal)
                }
                for oi in order_full.order_items
            ]
        }

        # Send email to user
        await send_order_picked_email(
            to_email=order_full.user.email,
            order=email_payload
        )



    # 4. Fetch full order with relationships for response
    full_result = await db.execute(
        select(Order)
        .where(Order.id == order.id)
        .options(
            selectinload(Order.user),
            selectinload(Order.shop),
            selectinload(Order.order_items).selectinload(OrderItem.item)
        )
    )

    return full_result.scalars().first()


