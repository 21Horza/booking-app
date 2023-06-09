from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.domain.shared.config.config import settings
from app.presentation.services.users_service import UsersService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_pwd_hash(pwd: str) -> str:
    return pwd_context.hash(pwd)

def verify_pwd(pwd: str, hashed_pwd: str) -> bool:
    return pwd_context.verify(pwd, hashed_pwd)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt

async def auth_user(email: EmailStr, password: str):
    candidate = await UsersService.get_one_or_none(email=email)
    if candidate and verify_pwd(password, candidate.hashed_password):
        return candidate