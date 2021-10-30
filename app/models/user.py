from app.shared.mongodb import mongo
from mongoengine import StringField


class User(mongo.Document):
    first_name = StringField()
    last_name = StringField()
    email = StringField()
