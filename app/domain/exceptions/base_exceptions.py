from fastapi import HTTPException


class ClientErrorException(HTTPException):
    status_code = 400
    detail = ""
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)