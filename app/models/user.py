from app.shared.database import db
from mongoengine import StringField


class User(db.Document):
    first_name = StringField()
    last_name = StringField()
    email_addr = StringField()
