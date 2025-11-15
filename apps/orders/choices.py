from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentChoice(models.TextChoices):
    """Gender choices"""

    AKBANK = "akbank", _("Akbank")
    Pasha = "pasha", _("Pasha")
    COD = "cod", _("Cash on Delivery")

class CurrencyChoice(models.TextChoices):
    AZN = "azn", _("AZN")
    TL = "tl", _("TL")


class StatusChoice(models.TextChoices):
    IN_PROGRESS = "in_progress", _("In Progress")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")
    ERROR = "error", _("Error")
    SUCCESS = "success", _("Success")