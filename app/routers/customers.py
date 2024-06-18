from fastapi import APIRouter, Depends, HTTPException, status
from app.models.customers import Customer 
from app.schemas.customer import  CustomerRead, CustomerCreate
import httpx
from app.utils import verify_token, oauth2_scheme, get_current_user
from typing import List
from datetime import timedelta, datetime
from app.config import settings
from jose import jwt



customer_R = APIRouter()



@customer_R.get("/customer/", response_model=List[CustomerRead])
def read_customers(current_user: Customer = Depends(get_current_user)):
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

@customer_R.delete("/customer/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(customer_id: int, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    verify_token(token, credentials_exception)

    # Buscar el cliente en la base de datos
    customer = Customer.get_or_none(Customer.id == customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Eliminar el cliente de la tabla Customer
    customer.delete_instance()

    # Hacer una petición HTTP DELETE a la API de autenticación para eliminar al usuario
    try:
        async with httpx.AsyncClient() as client:
            auth_response = await client.delete(f"http://localhost:8000/auth/users/{customer.username}")
            auth_response.raise_for_status()  # Asegurarse de que se lanza una excepción en caso de un código de estado HTTP de error
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Error al eliminar el usuario de la API de autenticación")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {exc}")

    return {"detail": "Customer deleted successfully"}
