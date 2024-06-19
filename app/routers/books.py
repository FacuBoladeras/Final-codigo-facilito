from fastapi import APIRouter, HTTPException, Depends, Request, Query
from app.models.books import Book
from app.schemas.book import BookCreate, BookRead
from typing import List
from app.utils import verify_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse

books_R = APIRouter()
templates = Jinja2Templates(directory="app/routers/templates")

# Endpoints que requieren autenticación

@books_R.post("/books/", response_model=BookRead)
def create_book(book: BookCreate):
    try:
        db_book = Book.create(**book.dict())
        return db_book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@books_R.get("/GetBooksJ/", response_model=List[BookRead])
def read_books(token: str = Query(..., description="JWT Token")):
    try:
        # Verificar el token
        user = verify_token(token)        
        books = Book.select()
        return list(books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


