from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.user import User
from app.models.enums import UserType
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            raise cred_exception
    except JWTError:
        raise cred_exception

    user = await db.get(User, user_id)

    if not user:
        raise cred_exception

    return user


def require_role(role: UserType):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.user_type != role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires {role} role"
            )
        return user
    return role_checker
