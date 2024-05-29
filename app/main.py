from fastapi import FastAPI
from app.routers import books, customers
from app.database import connect_db, close_db, database
from app.models.book import Book
from app.models.customer import Customer

app = FastAPI()

app.include_router(books.router)
app.include_router(customers.router)

@app.on_event("startup")
def startup():
    connect_db()
    # Crear tablas si no existen
    database.create_tables([Book, Customer], safe=True)

@app.on_event("shutdown")
def shutdown():
    close_db()
