from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.shop import Shop
from app.schemas.shop import ShopResponse, ShopCreate, ShopUpdate
from app.auth.dependencies import require_shop_owner


router = APIRouter(prefix="/shops", tags=["shops"])


# create shop owner only
@router.post("/create", response_model=ShopResponse)
async def create_shop(
    data: ShopCreate,
    current_user = Depends(require_shop_owner),
    db: AsyncSession = Depends(get_db)
):
    new_shop = Shop(
        name = data.name,
        description = data.description,
        address = data.address,
        phone = data.phone,
        owner_id = current_user.id
    )

    db.add(new_shop)
    await db.commit()
    await db.refresh(new_shop)

    return new_shop


# GET shops owned by current user
@router.get("/my-shop", response_model=list[ShopResponse])
async def get_my_shops(
    current_user = Depends(require_shop_owner),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Shop).where(Shop.owner_id == current_user.id)
    )

    shops = result.scalars().all()

    return shops

# GET all shops
@router.get("/all-shops")
async def get_all_shops(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Shop))
    shops = result.scalars().all()

    return shops



# UPDATE shop (only owner)
@router.put("/{shop_id}", response_model=ShopResponse)
async def update_shop(
    shop_id: int,
    data: ShopUpdate,
    current_user = Depends(require_shop_owner),
    db: AsyncSession = Depends(get_db)
):
    # find shop
    result = await db.execute(select(Shop).where(Shop.id == shop_id))

    shop = result.scalar_one_or_none()

    if not shop:
        raise HTTPException(
            status_code=400,
            detail="Shop not found"
        )    
    
    if shop.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not the owner of this shop"
        )
    
    # update field
    updated_data = data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(shop, key, value)

    await db.commit()
    await db.refresh(shop)
    return shop

    


