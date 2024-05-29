from fastapi import APIRouter
from app.models.books import Book 
from app.schemas.book import BookCreate, BookRead
from typing import List

books_R = APIRouter()

@books_R.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    db_book = Book.create(**book.dict())
    return db_book

@books_R.get("/books/", response_model=List[BookRead])
def read_books():
    books = Book.select()
    return list(books)