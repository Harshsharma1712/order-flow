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
