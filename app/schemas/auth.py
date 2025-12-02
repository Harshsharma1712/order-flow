from pydantic import BaseModel, EmailStr
from app.models.enums import UserType

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    user_type: UserType = UserType.NORMAL

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
