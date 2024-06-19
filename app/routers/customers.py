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



@customer_R.delete("/customer/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(username: str, token: str = Depends(oauth2_scheme)):
    verify_token(token)

    # Buscar el cliente en la base de datos por username
    customer = Customer.get_or_none(Customer.username == username)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Eliminar el cliente de la tabla Customer
    customer.delete_instance()

    # Hacer una petición HTTP DELETE a la API de autenticación para eliminar al usuario
    try:
        async with httpx.AsyncClient() as client:
            auth_response = await client.delete(f"http://localhost:8000/auth/users/{username}")
            auth_response.raise_for_status()  # Asegurarse de que se lanza una excepción en caso de un código de estado HTTP de error
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Error al eliminar el usuario de la API de autenticación")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {exc}")

    return {"detail": "Customer deleted successfully"}