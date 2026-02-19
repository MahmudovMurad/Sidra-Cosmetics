from django.shortcuts import render
from apps.products.models import Category, Product, ProductImage
from apps.mainapp.models import About
from django.db.models import Value, F, DecimalField, Prefetch
from django.db.models.functions import Coalesce
from django.utils import translation

# Create your views here.


def index_view(request):
    categories = Category.objects.only('id', 'name', 'parent_id').order_by('name')[:50]
    lang = translation.get_language()
    
    price_field_map = {
        "az": ("price_az", "discount_az"),
        "tr": ("price_tr", "discount_tr"),
        "en": ("price", "discount"),
    }
    price_field, discount_field = price_field_map.get(lang, ("price", "discount"))
    
    # 1. Base optimized query
    base_products = Product.objects.select_related("category").only(
        'id', 'name', 'category__name', 'category__id',
        price_field, discount_field, 'is_best_seller', 'created_at'
    ).prefetch_related(
        Prefetch(
            "productimage_set",
            queryset=ProductImage.objects.only("id", "image", "product_id").order_by('id')
        )
    ).annotate(
        # 2. Annotate generic fields so the template doesn't trigger deferred DB lookups
        current_price=F(price_field),
        current_discount=F(discount_field),
        final_price=F(price_field) - Coalesce(F(discount_field), Value(0), output_field=DecimalField())
    )

    context = {
        "categories": categories,
        # 3. Add limits! Don't load the entire database on the home page.
        "products": base_products.order_by("-created_at")[:12],
        "best_sellers": base_products.filter(is_best_seller=True).order_by("-created_at")[:10]
    }
    return render(request, "mainapp/index.html", context)


def about_view(request):
    about = About.get_solo()
    context = {"about": about}
    return render(request, "mainapp/about.html", context)