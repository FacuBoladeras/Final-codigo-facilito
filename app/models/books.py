from peewee import Model, CharField, IntegerField
from app.database import database

class Book(Model):
    title = CharField()
    author = CharField()
    quantity = IntegerField()
    gender = CharField()

    class Meta:
        database = database