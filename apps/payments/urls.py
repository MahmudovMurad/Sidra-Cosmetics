from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("akbank/callback/", views.akbank_callback_handler_view, name="akbank-callback"),
]