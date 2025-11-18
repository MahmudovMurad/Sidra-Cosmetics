from django.contrib import admin
from apps.mainapp.models import Settings, About

# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "address", "instagram", "facebook", "tiktok")



@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    ...