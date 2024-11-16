from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ref import User, ReferralCode


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_id(self, id: int):
        query = select(User).where(User.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user_data):
        new_user = User(**user_data.dict())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user


class ReferralCodeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_referral_code(self, referral_code_data, user):
        new_referral_code = ReferralCode(**referral_code_data.dict(), user_id=user.id)
        self.db.add(new_referral_code)
        await self.db.commit()
        await self.db.refresh(new_referral_code)
        return new_referral_code

    async def get_active_referral_code_by_user(self, user):
        query = select(ReferralCode).where(ReferralCode.user_id == user.id, ReferralCode.is_active == 1)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def deactivate_referral_code(self, referral_code):
        referral_code.is_active = 0
        await self.db.commit()