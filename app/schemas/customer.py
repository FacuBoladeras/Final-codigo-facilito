from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class CustomerCreate(BaseModel):
    username: str
    email: str
    password: str

class CustomerRead(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    
class CustomerUpdateRequest(BaseModel):
    username: str = None
    email: EmailStr = None