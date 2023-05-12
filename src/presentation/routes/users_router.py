from fastapi import APIRouter, HTTPException, status, Response
from app.infrastructure.identityProviders.password.auth import auth_user, create_access_token, get_pwd_hash, verify_pwd
from app.application.entities.users.schema.user_schema import SUserAuth
from ..services.users_service import UsersService

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)

@router.post("/register")
async def register_user(user_data: SUserAuth):
    candidate = await UsersService.find_one_or_none(email=user_data.email)
    if candidate:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    hashed_pwd = get_pwd_hash(user_data.pwd)
    await UsersService.add(email=user_data.email, hashed_password=hashed_pwd)

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    candidate = await auth_user(user_data.email, user_data.pwd)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({
        "sub": candidate.id
    })
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}
