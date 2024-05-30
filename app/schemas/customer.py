from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: int


class CustomerRead(BaseModel):
    id: int
    name: str
    email: str
    phone: int

    class Config:
        orm_mode: True
