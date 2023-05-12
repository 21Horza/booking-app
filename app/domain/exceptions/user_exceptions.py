from fastapi import status
from .base_exceptions import ClientErrorException

class UserAlreadyExistsExeption(ClientErrorException):
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",


class IncorrectEmailOrPwdException(ClientErrorException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
