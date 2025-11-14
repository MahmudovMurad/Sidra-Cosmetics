from django.db import models
from apps.utils.models.mixins import TrackedModelMixin
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

def upload_to_products(instance, filename):
    return f"products/product_{instance.product.id}/{filename}"

class Category(MPTTModel, TrackedModelMixin):
    name = models.CharField(max_length=300)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Category(name={self.name})"

    class Meta:
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ['name']



class Product(TrackedModelMixin):
    name = models.CharField(max_length=300)
    category = models.ForeignKey("products.Category", on_delete=models.PROTECT)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    description = RichTextField()
    is_best_seller = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price})"

    class Meta:
        verbose_name_plural = "Products"

    @property
    def first_product_image(self):
        return self.productimage_set.first().image.url if self.productimage_set.exists() else None

    @property
    def second_product_image(self):
        return self.productimage_set.all()[1].image.url if self.productimage_set.count() > 1 else self.first_product_image

    @property
    def total_price(self):
        return (self.price - self.discount) if self.discount else self.price


class ProductImage(TrackedModelMixin):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_products)

    def __str__(self):
        return self.product.name

    def __repr__(self):
        return f"ProductImage(product={self.product.id})"

    class Meta:
        verbose_name_plural = "Product Images"