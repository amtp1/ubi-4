from datetime import datetime as dt

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.contrib.auth import login, logout

from .models import *


def index(request):
    if request.user.is_authenticated:
        return redirect("profile")
    return redirect("login_user")

def profile(request):
    if not request.user.is_authenticated:
        return redirect("login_user")
    user_pk = request.session["_auth_user_id"]
    auth_user: QuerySet = User.objects.get(pk=user_pk)
    user_data: QuerySet = UserData.objects.get(pk=user_pk)
    bomber_data: QuerySet = BomberData.objects.get(username=str(auth_user.username))
    data: dict = dict(zip(["auth_user", "user_data", "bomber_data"], [auth_user, user_data, bomber_data]))
    return render(request, "profile.html", data)

def login_user(request):
    message: str = ""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if not username or not password:
            message: str = "Поля не должны оставаться пустыми!"
            data: dict = dict(zip(["message"], [message]))
        else:
            user: QuerySet = User.objects.filter(username=username, password=password)
            if user.exists():
                user: QuerySet = user.get()
                user.last_login = dt.now()
                user.save()
                login(request, user)
                return redirect("profile")
            else:
                message: str = "Пользователь не существует!"
    data = dict(zip(["message"], [message]))
    return render(request, "login.html", data)

def logout_user(request):
    logout(request)
    return redirect("index")