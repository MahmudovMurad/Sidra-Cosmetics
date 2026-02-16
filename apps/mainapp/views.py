from django.shortcuts import render
from apps.products.models import Category, Product, ProductImage
from apps.mainapp.models import About
from django.db.models import Value, F, DecimalField, Prefetch
from django.db.models.functions import Coalesce
from django.utils import translation

# Create your views here.


def index_view(request):
    # Optimize categories query
    categories = Category.objects.only('id', 'name', 'parent_id').order_by('name')[:50]
    
    lang = translation.get_language()  # e.g. "az", "tr", "en"

    # map language codes to model fields
    price_field_map = {
        "az": ("price_az", "discount_az"),
        "tr": ("price_tr", "discount_tr"),
        "en": ("price", "discount"),  # fallback
    }
    price_field, discount_field = price_field_map.get(lang, ("price", "discount"))
    
    # Optimize product query - select only needed fields and prefetch images
    products = Product.objects.select_related("category").only(
        'id', 'name', 'category__name', 'category__id',
        price_field, discount_field, 'is_best_seller', 'created_at'
    ).prefetch_related(
        Prefetch(
            "productimage_set",
            queryset=ProductImage.objects.only("id", "image", "product_id").order_by('id')
        )
    ).annotate(
        final_price=F(price_field) - Coalesce(F(discount_field), Value(0), output_field=DecimalField())
    ).order_by("-created_at")

    context = {
        "categories": categories,
        "products": products,
        "best_sellers": products.filter(is_best_seller=True)
    }
    return render(request, "mainapp/index.html", context)


def about_view(request):
    about = About.get_solo()
    context = {"about": about}
    return render(request, "mainapp/about.html", context)