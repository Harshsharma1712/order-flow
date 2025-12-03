from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import verify_password, hash_password
from app.core.jwt import create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest, Token
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])


# Register a user 
@router.post("/register")
async def register_user(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    # Check if email exists
    result = await db.execute(select(User).where(User.email == data.email))

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email alrady registered"
        )
    
    # hash password
    hashed = hash_password(data.password)

    new_user = User(
        email = data.email,
        username = data.username,
        hashed_password = hashed,
        full_name = data.full_name,
        user_type = data.user_type
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "message": "User register successfully",
        "user_id": new_user.id,
        "email": new_user.email
    }


# login a user
@router.post("/login", response_model=Token)
async def login_user(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == data.email))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=400,
            detail= "User not found"
        )
    
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail= "Password and Hashed pass not match verify"
        )
    
    # create a jwt
    token = create_access_token({
        "user_id": user.id,
        "user_type": user.user_type.value
    })

    response = JSONResponse({
        "message": "Login successfully",
        "token": token
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES* 60
    )

    return response


# logout
@router.post("/logout")
async def logout_user(response: Response):

    response.delete_cookie("access_token", httponly=True, samesite="lax")

    return {
        "message": "Logged out successfully"
    }






