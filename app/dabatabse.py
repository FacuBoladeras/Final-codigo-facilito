from peewee import MySQLDatabase
from app.config import settings

# Conexión a la base de datos
database = MySQLDatabase(
    settings.database_name,
    user=settings.database_user,
    password=settings.database_password,
    host=settings.database_host,
    port=settings.database_port
)

def connect_db():
    if not database.is_closed():
        database.connect()

def close_db():
    if not database.is_closed():
        database.close()
