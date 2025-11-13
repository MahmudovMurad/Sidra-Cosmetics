from django.contrib import admin
from apps.mainapp.models import Settings

# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address", "instagram", "facebook", "tiktok")
