from fastapi import Depends, Request
from jose import ExpiredSignatureError,JWTError, jwt

from app.domain.exceptions.token_exceptions import (
    IncorrectTokenFormatException,
    TokenExpiredException,
    TokenIsAbsentException,
    UserIsNotAuth,
)
from app.domain.shared.config.config import settings
from app.presentation.services.users_service import UsersService


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise TokenIsAbsentException
    return token
    
async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )

    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotAuth
    user = await UsersService.get_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotAuth

    return user