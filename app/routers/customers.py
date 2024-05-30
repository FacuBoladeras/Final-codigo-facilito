from fastapi import APIRouter
from app.models.customers import Customer 
from app.schemas.customer import CustomerCreate, CustomerRead
from typing import List

customer_R = APIRouter()

@customer_R.post("/customerP/", response_model=CustomerRead)
def create_book(customer: CustomerCreate):
    db_book = Customer.create(**customer.dict())
    return db_book

@customer_R.get("/customer/", response_model=List[CustomerRead])
def read_books():
    books = Customer.select()
    return list(books)