from django.db import models
from apps.utils.models.mixins import TrackedModelMixin

# Create your models here.


class Transaction(TrackedModelMixin):
    user_ip = models.CharField(max_length=500)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True)

    transaction_uuid = models.CharField(max_length=120)
    order_uuid = models.CharField(max_length=120)
    description = models.TextField()
    amount = models.DecimalField(max_digits=30, decimal_places=2)

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.transaction_uuid

    class Meta:
        verbose_name_plural = "United Payment Transactions"
