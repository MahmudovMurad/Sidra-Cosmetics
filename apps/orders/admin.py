from django.contrib import admin
from apps.orders.models import (
    Order, OrderItem
)

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "email",
        "phone",
        "is_delivery",
        "address",
        "pay_choice",
        "is_paid",
        "is_completed",
        "created_at"
    )
    list_filter = ("pay_choice", "is_paid", "is_paid", "is_completed", "created_at")
    search_fields = ("name", "surname", "email", "phone")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    list_filter = ("order__is_paid", "order__pay_choice")
    search_fields = (
        "product__name",
        "order__name",
        "order__surname",
        "order__email",
        "order__phone",
    )