from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.schemas.ref_py import UserCreate, UserResponse, Token, ReferralCodeCreate, ReferralCodeResponse, ReferralsResponse
from app.servises.ref_ser import AuthService, ReferralService
from app.repository.repositories import UserRepository
from app.servises.secr import create_access_token, get_current_user
from app.models.database import init_db, close_db, async_session


app = FastAPI(
        title="My API",
        description="простой RESTful API сервис для реферальной системы.",
        version="1.0.0",
    )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
def read_root():
    return {"Test": "Test"}


@app.on_event("startup")
async def startup():
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    await close_db()


async def get_db() -> AsyncSession:
    async with async_session as session:
        yield session


@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    new_user = await auth_service.register_user(user)
    return UserResponse(id=new_user.id, email=new_user.email)


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)

    user = await auth_service.login_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@app.post("/referral_code/create", response_model=ReferralCodeResponse)
async def create_referral_code(referral_code: ReferralCodeCreate, db: AsyncSession = Depends(get_db),
                               token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token=token, db=db)

    referral_service = ReferralService(db)
    new_referral_code = await referral_service.create_referral_code(referral_code, current_user)
    return {"code": new_referral_code.code,
            "expires_at": new_referral_code.expires_at.isoformat(),
            "is_active": new_referral_code.is_active}


@app.delete("/referral_code/delete")
async def delete_referral_code(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token=token, db=db)

    referral_service = ReferralService(db)

    if await referral_service.delete_referral_code(current_user):
        return {"message": "Referral code deleted successfully."}


@app.get("/referral_code/{email}", response_model=ReferralCodeResponse)
async def get_referral_code(email: str, db: AsyncSession = Depends(get_db)):
    user_repo = UserRepository(db)

    referrer_user = await user_repo.get_user_by_email(email=email)

    referral_service = ReferralService(db)

    if referrer_user:
        active_referral_code = await referral_service.get_active_referral_code(referrer_user)

        if active_referral_code:
            return {"code": active_referral_code.code,
                    "expires_at": active_referral_code.expires_at.isoformat(),
                    "is_active": active_referral_code.is_active}

    raise HTTPException(status_code=404, detail="No referral code found for this email.")


@app.get("/referrals/{referrer_id}", response_model=ReferralsResponse)
async def get_referrals(referrer_id: int, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token=token, db=db)

    # Проверка прав доступа
    if current_user.id != referrer_id:
        raise HTTPException(status_code=403, detail="You are not authorized to view these referrals.")

    referral_service = ReferralService(db)
    referrals = await referral_service.get_referrals(referrer_id)

    return ReferralsResponse(
        referrals=[UserResponse(id=referral.id, email=referral.email) for referral in referrals])
