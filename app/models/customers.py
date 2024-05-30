from peewee import Model, CharField, IntegerField
from app.database import database

class Customer(Model):
    name = CharField()
    email = CharField()
    phone = IntegerField()

    class Meta:
        database = database