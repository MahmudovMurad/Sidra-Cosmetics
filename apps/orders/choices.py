from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentChoice(models.TextChoices):
    """Gender choices"""

    AKBANK = "akbank", _("Akbank")
    Pasha = "pasha", _("Pasha")
    COD = "cod", _("Cash on Delivery")