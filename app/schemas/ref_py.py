from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # Минимальная длина пароля 8 символов
    referrer_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class ReferralCodeCreate(BaseModel):
    code: str
    expires_at: datetime


class ReferralCodeResponse(BaseModel):
    code: str
    expires_at: datetime
    is_active: bool


class ReferralsResponse(BaseModel):
    referrals: List[UserResponse]