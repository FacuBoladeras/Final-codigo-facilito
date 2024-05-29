from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    quantity: int

class BookCreate(BookBase):
    pass

class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True
