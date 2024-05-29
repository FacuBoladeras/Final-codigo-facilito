from peewee import Model, CharField
from app.database import database

class Customer(Model):
    name = CharField()
    email = CharField()
    phone_number = CharField()

    class Meta:
        database = database