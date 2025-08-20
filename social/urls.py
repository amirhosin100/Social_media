from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from .views import MyConfirm

app_name = "social"

urlpatterns = [
    path("",views.main,name="main"),
    path("login/",auth_views.LoginView.as_view(),name="login"),
    path("register/",views.register,name="register"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("ticket/",views.ticket,name="ticket"),

    #password-reset
    path("password-reset/",auth_views.PasswordResetView.as_view(success_url="done",
                        html_email_template_name="registration/password_reset_email.html"),name="password_reset"),
    path("password-reset/done",auth_views.PasswordResetDoneView.as_view(),name="password_rest_done"),
    path("password-reset-confrim/<uidb64>/<token>",MyConfirm.as_view(success_url=reverse_lazy("social:main")),name="password_reset_confirm"),

    path("posts/",views.PostListView.as_view(),name="posts"),
    path("posts/detail/<int:pk>",views.PostDetail.as_view(),name="detail"),
    path("create-post/",views.create_post,name="create_post"),
    path("search-posts/",views.search_post,name="search_post"),


]