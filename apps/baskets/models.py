from django.db import models
from apps.utils.models.mixins import TrackedModelMixin

# Create your models here.



class Basket(TrackedModelMixin):
    user_ip = models.CharField(max_length=500, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_ip

    class Meta:
        verbose_name_plural = "Baskets"
        indexes = [
            models.Index(fields=['is_active', 'user_ip']),
        ]

    @property
    def total_price(self):
        return sum([basket_item.total_price for basket_item in self.basketitem_set.all()])



class BasketItem(TrackedModelMixin):
    basket = models.ForeignKey("baskets.Basket", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} qty"

    class Meta:
        verbose_name_plural = "Basket Items"

    @property
    def total_price(self):
        return float(self.product.total_price) * self.quantity