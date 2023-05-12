from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime
from app.domain.entities.users.model.users_model import Users
from app.domain.exceptions.token_exceptions import TokenExpiredException, TokenIsAbsentException, IncorrectTokenFormatException, UserIsNotAuth
from app.infrastructure.database.config import settings
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

    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()): 
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id: 
        raise UserIsNotAuth
    user = await UsersService.find_by_id(int(user_id))
    if not user: 
        raise UserIsNotAuth

    return user

async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role != "admin":
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return current_user