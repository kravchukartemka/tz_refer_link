from jwt import PyJWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.repositories import UserRepository

SECRET_KEY = "most_secret_key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# принимает пароль текст, возвращает хеш
def get_password_hash(password):
    return pwd_context.hash(password)


# сравнивает хеш с хешем от введёного пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# создание асес токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# возвращает информацию о пользователе
def get_current_user(token: str, db: AsyncSession):
    try:
        # Декодируем токен, извлекая данные
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # Предполагаем, что ID пользователя хранится в поле "sub"

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = UserRepository(db)
        user = user.get_user_by_id(user_id)
        return user

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
