"""Top-level URL configuration for Record Shelf."""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from main_app import views as main_views


urlpatterns = [
    path("admin/", admin.site.urls),

    # Public landing page
    path("", main_views.home, name="home"),

    # Auth: built-in login/logout + custom signup live in the accounts app
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/", include("accounts.urls")),

    # Album CRUD
    path("albums/", include("main_app.urls", namespace="albums")),
]
