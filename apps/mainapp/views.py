from django.shortcuts import render
from apps.products.models import Category, Product
from apps.mainapp.models import About
from django.db.models import Value, F, DecimalField
from django.db.models.functions import Coalesce
from django.utils import translation

# Create your views here.


def index_view(request):
    categories = Category.objects.all()
    lang = translation.get_language()  # e.g. "az", "tr", "en"

    # map language codes to model fields
    price_field_map = {
        "az": ("price_az", "discount_az"),
        "tr": ("price_tr", "discount_tr"),
        "en": ("price", "discount"),  # fallback
    }
    price_field, discount_field = price_field_map.get(lang, ("price", "discount"))
    products = Product.objects.annotate(
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