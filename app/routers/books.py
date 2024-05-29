from fastapi import APIRouter
from app.models.book import Book
from app.schemas.book import BookCreate, BookRead
from typing import List

router = APIRouter()

@router.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    db_book = Book.create(**book.dict())
    return db_book

@router.get("/books/", response_model=List[BookRead])
def read_books():
    books = Book.select()
    return list(books)
