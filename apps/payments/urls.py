from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("callback/", views.callback_view, name="callback"),
    path("success/", views.payment_success_view, name="success"),
    path("failure/", views.payment_failure_view, name="failure"),
]