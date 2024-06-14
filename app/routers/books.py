from fastapi import APIRouter, HTTPException,Depends
from app.models.books import Book 
from app.schemas.book import BookCreate, BookRead
from typing import List
from app.utils import verify_token

books_R = APIRouter()

@books_R.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    db_book = Book.create(**book.dict())
    return db_book

@books_R.get("/books/", response_model=List[BookRead], dependencies=[Depends(verify_token)])
def read_books(username: str = Depends(verify_token)):
    try:
        books = Book.select()
        return list(books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@books_R.get("/books/{id}", response_model=BookRead, dependencies=[Depends(verify_token)])
def read_book(id: int, username: str = Depends(verify_token)):
    try:
        book = Book.get(Book.id == id)
        return book
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")


# Nuevo enrutador para endpoints que no requieren autenticación
booksF = APIRouter()


@booksF.get("/books/", response_model=List[BookRead])
async def read_books():
    try:
        books = Book.select()
        return list(books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@booksF.get("/booksF/{id}", response_model=BookRead)
def read_book_without_auth(id: int):
    try:
        book = Book.get(Book.id == id)
        return book
    except Book.DoesNotExist:
        raise HTTPException(status_code=404, detail="Book not found")