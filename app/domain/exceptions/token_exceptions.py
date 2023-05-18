from fastapi import status
from .base_exceptions import ClientErrorException

class TokenExpiredException(ClientErrorException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired",

class TokenIsAbsentException(ClientErrorException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is absent",


class IncorrectTokenFormatException(ClientErrorException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect token format",


class UserIsNotAuth(ClientErrorException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not authorized",