from fastapi import APIRouter, HTTPException
from app.models.books import Book 
from app.schemas.book import BookCreate, BookRead
from typing import List

books_R = APIRouter()

@books_R.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    db_book = Book.create(**book.dict())
    return db_book

@books_R.get("/book/", response_model=List[BookRead])
def read_books():
    books = Book.select()
    return list(books)

@books_R.get("/book/{id}", response_model=BookRead)
def read_book(id: int):
    try:
        book = Book.get(Book.id == id)
        return book
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")