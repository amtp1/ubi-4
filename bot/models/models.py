from datetime import datetime as dt
from orm import Model, DateTime, String, Integer, Float, ModelRegistry, ForeignKey, Boolean

from objects.globals import db

models = ModelRegistry(database=db)

class AuthUser(Model):
    tablename = "auth_user"
    registry = models

    fields = {
        "id": Integer(primary_key=True),
        "password": String(max_length=128, allow_null=False),
        "last_login": DateTime(allow_null=True),
        "is_superuser": Boolean(default=False, allow_null=False),
        "username": String(max_length=150, allow_null=False),
        "last_name": String(max_length=150, allow_null=True),
        "email": String(allow_blank=True, max_length=254, allow_null=False),
        "is_staff": Boolean(default=False, allow_null=False),
        "is_active": Boolean(default=True, allow_null=False),
        "date_joined": DateTime(default=dt.now(), allow_null=False),
        "first_name": String(max_length=150, allow_null=True),
    }

    def __repr__(self):
        return "<%s>" % (self.id,)

class UserData(Model):
    tablename = "core_userdata"
    registry = models

    fields = {
        "id": Integer(primary_key=True),
        "balance": Float(default=0.0),
        "language": String(max_length=16, allow_null=True),
        "username": String(max_length=150, allow_null=True),
        "is_bomber": Boolean(allow_null=True),
        "is_blocked": Boolean(allow_null=True),
        "auth_user_id": ForeignKey(AuthUser),
    }

    def __repr__(self):
        return "<%s>" % (self.id,)

class BomberData(Model):
    tablename = "core_bomberdata"
    registry = models

    fields = {
        "id": Integer(primary_key=True),
        "username": String(max_length=150),
        "circles": String(max_length=255),
        "last_phone": String(max_length=128, allow_null=True),
        "last_launch": DateTime(allow_null=True),
        "created": DateTime(default=dt.now())
    }

    def __repr__(self):
        return "<%s>" % (self.id,)