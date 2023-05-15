from pydantic import BaseModel, EmailStr

class SUserAuth(BaseModel):
    id: int
    email: EmailStr
    pwd: str

    class Config:
        orm_mode = True