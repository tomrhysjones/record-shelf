from django.urls import path

from . import views


app_name = "albums"


urlpatterns = [
    path("", views.album_list, name="list"),
    path("mine/", views.my_shelf, name="my_shelf"),
    path("new/", views.album_create, name="create"),
    path("<int:pk>/", views.album_detail, name="detail"),
    path("<int:pk>/edit/", views.album_update, name="update"),
    path("<int:pk>/delete/", views.album_delete, name="delete"),
]
