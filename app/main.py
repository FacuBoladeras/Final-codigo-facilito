from fastapi import FastAPI
from .routers.books import books_R
from .routers.customers import customer_R
from .models.books import Book 
from .models.customers import Customer
from .database import connect_db, close_db, database
from .models.books import Book

# uvicorn app.main:app --reload --port 8001

app = FastAPI()

app.include_router(books_R)
app.include_router(customer_R)

@app.on_event("startup")
def startup():
    connect_db()
    # Crear tablas si no existen
    database.create_tables([Book], safe=True)
    database.create_tables([Customer], safe=True)

@app.on_event("shutdown")
def shutdown():
    close_db()