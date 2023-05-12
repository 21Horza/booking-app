from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.application.entities.users.model.users_model import Users
from app.infrastructure.identityProviders.password.auth import auth_user, create_access_token, get_pwd_hash, verify_pwd
from app.application.entities.users.schema.user_schema import SUserAuth
from ..services.users_service import UsersService
from ..middlewares.users_middleware import get_current_user, get_current_admin_user


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
        "sub": str(candidate.id)
    })
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return HTTPException(status_code=status.HTTP_200_OK)

@router.get("/profile")
async def get_user_profile(current_user: Users = Depends(get_current_user)):
    return current_user

# @router.get("/users")
# async def get_all_users(current_user: Users = Depends(get_current_admin_user)):
#     return await UsersService.get_all()