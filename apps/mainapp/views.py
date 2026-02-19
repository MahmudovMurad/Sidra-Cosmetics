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
    
    # Optimize product query - select only needed fields and prefetch images
    products = Product.objects.select_related("category").only(
        'id', 'name', 'category__name', 'category__id',
        "price", "price_az", "price_tr", "price_en",
        "discount", "discount_az", "discount_tr", "discount_en",
        'is_best_seller', 'created_at'
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