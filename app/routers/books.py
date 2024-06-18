from fastapi import APIRouter, HTTPException, Depends, Request
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

@books_R.get("/books/", response_model=List[BookRead])
def read_books(token: str = Depends(verify_token)):
    try:
        books = Book.select()
        return list(books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoints que no requieren autenticación

booksF = APIRouter()

@books_R.get("/GetBooks/", response_class=HTMLResponse)
async def read_books_html(request: Request):
    try:
        books = Book.select()
        return templates.TemplateResponse("books.html", {
            "request": request,
            "title": "Books",
            "books": list(books)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@books_R.get("/GetBooksJ/", response_class=JSONResponse)
async def read_books_json():
    try:
        books = Book.select()
        books_list = [{"title": book.title, "author": book.author, "gender": book.gender} for book in books]
        return JSONResponse(content={"books": books_list})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))