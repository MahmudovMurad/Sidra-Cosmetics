from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Product, ProductImage, Category

# Register your models here.


class ImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent", "created_at", "updated_at")
    search_fields = ("name", "parent__name")
    mptt_level_indent = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "created_at")
    search_fields = ("name",)
    list_filter = ("category", "created_at")
    inlines = (ImageInline, )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "created_at")
    search_fields = ("product__name", )
    list_filter = ("product__category", )