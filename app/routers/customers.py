from fastapi import APIRouter, Depends, HTTPException, status
from app.models.customers import Customer 
from app.schemas.customer import CustomerCreate, CustomerRead
from app.utils import verify_token, oauth2_scheme
from typing import List

customer_R = APIRouter()


@customer_R.get("/customer/", response_model=List[CustomerRead])
def read_customers(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_token(token, credentials_exception)
    customers = Customer.select()
    return list(customers)



@customer_R.post("/customerP/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate):
    # Verificar si el cliente ya está registrado en la base de datos de Library
    if Customer.select().where(Customer.username == customer.username).exists():
        raise HTTPException(status_code=400, detail="Username already registered")
    if Customer.select().where(Customer.email == customer.email).exists():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_customer = Customer.create(**customer.dict())
    return db_customer