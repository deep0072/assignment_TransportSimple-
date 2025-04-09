from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path(f"auth/users/",RegisterView.as_view(), name="user-register"),
    path(f"auth/users/login",CustomLoginView.as_view(), name="user-register"),
    path(f"auth/users/logout",LogoutView.as_view(), name="user-logout"),

]
