from django.contrib.auth.models import User
from django.db import models

class UserData(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True)
    balance = models.FloatField(default=0.0, null=False)
    language = models.CharField(max_length=16, null=True)
    username = models.CharField(max_length=150, null=True)
    is_bomber = models.BooleanField(null=True)
    is_blocked = models.BooleanField(null=True)

class BomberData(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150)
    circles = models.CharField(max_length=255)
    last_phone = models.CharField(max_length=128, null=True)
    last_launch = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)