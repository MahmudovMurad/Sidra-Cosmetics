from django.contrib import admin
from django.core.cache import cache
from apps.mainapp.models import Settings, About, Banner

# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address", "instagram", "facebook", "tiktok")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete('site_settings')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        cache.delete('site_settings')



@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    ...


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete('site_banners')

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        cache.delete('site_banners')