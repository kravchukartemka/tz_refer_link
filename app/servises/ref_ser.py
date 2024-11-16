from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from app.models.ref import User
from app.repository.repositories import UserRepository, ReferralCodeRepository
from app.schemas.ref_py import UserCreate, Token
from app.servises.secr import get_password_hash, verify_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)

    async def register_user(self, user: UserCreate):
        existing_user = await self.user_repo.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(user.password)
        new_user = await self.user_repo.create_user(UserCreate(email=user.email, password=hashed_password))
        return new_user

    async def login_user(self, username: str, password: str):
        user = await self.user_repo.get_user_by_email(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        return user


class ReferralService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.referral_code_repo = ReferralCodeRepository(db)

    async def create_referral_code(self, referral_code_data, current_user):
        new_referral_code = await self.referral_code_repo.create_referral_code(referral_code_data, current_user)
        return new_referral_code

    async def delete_referral_code(self, current_user):
        active_referral_code = await self.referral_code_repo.get_active_referral_code_by_user(current_user)
        if active_referral_code:
            await self.referral_code_repo.deactivate_referral_code(active_referral_code)
            return True
        raise HTTPException(status_code=404, detail="No active referral code found.")

    async def get_active_referral_code(self, user):
        return await self.referral_code_repo.get_active_referral_code_by_user(user)

    async def get_referrals(self, referrer_id):
        query = select(User).where(User.referrer_id == referrer_id)
        result = await self.db.execute(query)
        return result.scalars().all()
