from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models import User
from app.auth.dependencies import require_role

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users


