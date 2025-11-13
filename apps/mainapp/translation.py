from modeltranslation.translator import TranslationOptions, register

from .models import Settings


@register(Settings)
class SettingsTranslationOptions(TranslationOptions):
    fields = (
        "short_description",
        "email",
        "address",
        "phone",
        "working_hours",
        "instagram",
        "facebook",
        "tiktok"
    )