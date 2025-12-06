from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.shop import Shop
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.auth.dependencies import require_shop_owner


router = APIRouter(prefix="/items", tags=["Items"])


# add item (shop_owner only, and must own the shop)
@router.post("/{shop_id}/add", response_model=ItemResponse)
async def add_item(
    shop_id: int,
    data: ItemCreate,
    current_user = Depends(require_shop_owner),
    db: AsyncSession = Depends(get_db)
):
    # Verify shop ownership
    result = await db.execute(select(Shop).where(Shop.id == shop_id))

    shop = result.scalar_one_or_none()

    if not shop:
        raise HTTPException(
            status_code=404,
            detail="Shop not found"
        )
    
    if shop.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail= "You are not the owner of this shop"
        )
    
    # create item
    new_item = Item(
        name = data.name,
        description = data.description,
        price = data.price,
        is_available = data.is_available,
        category = data.category,
        stock_quantity = data.stock_quantity,
        shop_id = shop_id
    )

    db.add(new_item)

    await db.commit()
    await db.refresh(new_item)

    return new_item

# update the item (only shop owner)
@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    current_user = Depends(require_shop_owner),
    db: AsyncSession = Depends(get_db)
):
    # fetch item
    result = await db.execute(select(Item).where(Item.id == item_id))

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    
    # Fetch shop to verify ownership
    result = await db.execute(select(Shop).where(Shop.id == item.shop_id))
    shop = result.scalar_one_or_none()

    if shop.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this shop"
        )
    
    # update filed
    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    
    return item



