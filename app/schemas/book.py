from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    quantity: int

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    quantity: int

    class Config:
        orm_mode: True
