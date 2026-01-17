from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import F, DecimalField, Value
from django.db.models.functions import Coalesce
from django.utils import translation
from apps.products.filters import filter_products
from django.core.paginator import Paginator


# Create your views here.


def product_list_view(request):
    categories = Category.objects.order_by("-created_at")

    lang = translation.get_language()  # e.g. "az", "tr", "en"

    # map language codes to model fields
    price_field_map = {
        "az": ("price_az", "discount_az"),
        "tr": ("price_tr", "discount_tr"),
        "en": ("price", "discount"),  # fallback
    }
    price_field, discount_field = price_field_map.get(lang, ("price", "discount"))
    products = Product.objects.select_related("category").prefetch_related("productimage").annotate(
        final_price=F(price_field) - Coalesce(F(discount_field), Value(0), output_field=DecimalField())
    ).order_by("-created_at")

    filtered_products, search_query_params = filter_products(
        queryset=products,
        query_params=request.GET
    )

    p = Paginator(filtered_products, 10)
    page = request.GET.get("page", 1)
    queryset = p.page(page)

    context = {
        "categories": categories,
        "products": queryset,
        "search_query_params": search_query_params,
        "search_param": "&".join(f"{k}={v}" for k, v in search_query_params.items())
    }
    return render(request, "products/list.html", context)



def product_detail_view(request, id):
    lang = translation.get_language()  # e.g. "az", "tr", "en"

    # map language codes to model fields
    price_field_map = {
        "az": ("price_az", "discount_az"),
        "tr": ("price_tr", "discount_tr"),
        "en": ("price", "discount"),  # fallback
    }
    price_field, discount_field = price_field_map.get(lang, ("price", "discount"))
    products = Product.objects.select_related("category").prefetch_related("productimage").annotate(
        final_price=F(price_field) - Coalesce(F(discount_field), Value(0), output_field=DecimalField())
    ).order_by("-created_at")

    product = get_object_or_404(products, id=id)
    context = {
        "product": product
    }
    return render(request, "products/detail.html", context)