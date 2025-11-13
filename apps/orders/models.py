from django.db import models
from apps.utils.models.mixins import TrackedModelMixin
from phonenumber_field.modelfields import PhoneNumberField
from apps.orders.choices import PaymentChoice

# Create your models here.


class Order(TrackedModelMixin):
    user_ip = models.CharField(max_length=500)
    name = models.CharField(max_length=300)
    surname = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=300)

    is_delivery = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

    pay_choice = models.CharField(max_length=300, choices=PaymentChoice.choices, default="cod")

    is_paid = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name_plural = "Orders"


class OrderItem(TrackedModelMixin):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = "Order Items"