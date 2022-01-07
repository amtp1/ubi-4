from django.contrib import admin

from .models import *

@admin.register(UserData)
class UserData(admin.ModelAdmin):
    list_display = ("id", "username", "balance", "language",)

@admin.register(BomberData)
class BomberData(admin.ModelAdmin):
    list_display = ("id", "username", "created",)