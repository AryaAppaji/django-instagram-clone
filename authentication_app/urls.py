from django.urls import path
from .views import loginUser, logoutUser

urlpatterns = [
    path("login/", loginUser),
    path("logout/", logoutUser),
]
