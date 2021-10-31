from mongoengine.queryset.manager import QuerySetManager
from mongoengine.document import Document
from mongoengine.fields import (
    IntField,
    ListField,
    EmailField,
    StringField,
    BooleanField,
    DateTimeField
)

from app.auth.roles import Role


class User(Document):

    objects = QuerySetManager()

    username = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    password_salt = StringField(required=True)
    roles = ListField(IntField(), required=True, default=[
        Role.UNPRIVILEGED
    ])

    created = DateTimeField(required=True)
    last_seen = DateTimeField(required=True)
    locked = BooleanField(required=True, default=False)

    firstname = StringField(max_length=64)
    lastname = StringField(max_length=64)
    email = EmailField(max_length=64)
