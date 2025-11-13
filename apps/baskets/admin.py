from django.contrib import admin
from .models import Basket, BasketItem

# Register your models here.

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ("user_ip", "is_active")
    list_filter = ("is_active", )


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ("basket", "product", "quantity")
    search_fields = ("product__name", )
    list_filter = ("basket__is_active", )
