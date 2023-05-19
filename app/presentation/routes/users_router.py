from fastapi import APIRouter, Depends, Response

from app.domain.entities.users.model.user_model import Users
from app.domain.entities.users.schema.user_schema import SUserAuth
from app.domain.exceptions.user_exceptions import (
    IncorrectEmailOrPwdException,
    UserAlreadyExistsExeption,
)
from app.infrastructure.identityProviders.password.auth import (
    auth_user,
    create_access_token,
    get_pwd_hash,
)

from ..middlewares.users_middleware import get_current_user
from ..services.users_service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    candidate = await UsersService.get_one_or_none(email=user_data.email)
    if candidate:
        raise UserAlreadyExistsExeption
    hashed_pwd = get_pwd_hash(user_data.pwd)
    await UsersService.add(email=user_data.email, hashed_password=hashed_pwd)

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    candidate = await auth_user(user_data.email, user_data.pwd)
    if not candidate:
        raise IncorrectEmailOrPwdException
    access_token = create_access_token({
        "sub": str(candidate.id)
    })
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

@router.get("/profile")
async def get_user_profile(current_user: Users = Depends(get_current_user)):
    return current_user
