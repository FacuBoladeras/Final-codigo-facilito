from pydantic import BaseModel

class CustomerCreate(BaseModel):
    username: str
    email: str
    password: str


class CustomerRead(BaseModel):
    id: int
    username: str
    email: str
    password: str

    class Config:
        orm_mode: True
