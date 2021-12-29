from django.urls import path, include
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("login", login_user, name="login_user"),
    path("profile", profile, name="profile"),
    path("logout", logout_user, name="logout_user")
]