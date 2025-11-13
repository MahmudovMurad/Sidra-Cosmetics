from django.urls import path
from . import views

app_name = "baskets"

urlpatterns = [
    path("", views.basket_list_view, name="list"),
    path("create/", views.basket_create_view, name="create"),
    path("delete/", views.basket_delete_view, name="delete"),
    path("remove/", views.basket_remove_view, name="remove"),
]