from django.db import models
from apps.utils.models.mixins import TrackedModelMixin
from ckeditor.fields import RichTextField

# Create your models here.


class Settings(TrackedModelMixin):
    short_description = models.TextField()

    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    working_hours = RichTextField()

    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name_plural = "Settings"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists."""
        if not self.pk and Settings.objects.exists():
            # If trying to create a new instance and one exists, raise error
            raise Exception("You can only have one Settings instance.")
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Get the single Settings instance, or create it if it doesn't exist."""
        try:
            obj = cls.objects.get()
            return obj
        except:
            return None
