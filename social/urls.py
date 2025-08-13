from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = "social"

urlpatterns = [
    path("",views.main,name="main"),
    path("login/",auth_views.LoginView.as_view(),name="login"),
    path("register/",views.register,name="register"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("ticket/",views.ticket,name="ticket"),
]