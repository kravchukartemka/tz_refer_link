from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.models.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class User(BaseModel):
    __tablename__ = 'users'

    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    referrals = relationship("User")


class ReferralCode(BaseModel):
    __tablename__ = 'referral_codes'

    code = Column(String, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    expires_at = Column(DateTime)
    is_active = Column(Integer)
    # is_active = Column(Boolean, default=True)
    # user = relationship("User", back_populates="referral_code")