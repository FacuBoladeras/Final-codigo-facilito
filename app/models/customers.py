from peewee import Model, CharField, IntegerField
from app.database import database


class Customer(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = database
        
