from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    quantity: int
    gender: str

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    quantity: int
    gender: str

    class Config:
        orm_mode: True
