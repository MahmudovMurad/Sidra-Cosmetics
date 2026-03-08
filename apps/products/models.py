from django.db import models
from apps.utils.models.mixins import TrackedModelMixin
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.functional import cached_property

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
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['name']),
        ]

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
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_best_seller', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

    @cached_property
    def first_product_image(self):
        """Get first product image using prefetched data to avoid N+1 queries"""
        # Access prefetched data directly without triggering new queries
        images = getattr(self, '_prefetched_objects_cache', {}).get('productimage_set')
        if images is None:
            # Fallback if not prefetched (shouldn't happen in optimized views)
            images = list(self.productimage_set.all()[:1])
        else:
            images = list(images)
        return images[0].image.url if images else None

    @cached_property
    def second_product_image(self):
        """Get second product image using prefetched data to avoid N+1 queries"""
        # Access prefetched data directly without triggering new queries
        images = getattr(self, '_prefetched_objects_cache', {}).get('productimage_set')
        if images is None:
            # Fallback if not prefetched
            images = list(self.productimage_set.all()[:2])
        else:
            images = list(images)
        if len(images) > 1:
            return images[1].image.url
        return self.first_product_image

    @property
    def total_price(self):
        return (self.price - (self.price * self.discount) / 100) if self.discount else self.price


class ProductImage(TrackedModelMixin):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_products)

    def __str__(self):
        return self.product.name

    def __repr__(self):
        return f"ProductImage(product={self.product.id})"

    def save(self, *args, **kwargs):
        # Auto-compress images on upload to prevent 13-17MB PNGs
        if self.image and hasattr(self.image, 'read'):
            from apps.utils.image import compress_image
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Product Images"
        ordering = ['id']  # Consistent ordering for prefetch