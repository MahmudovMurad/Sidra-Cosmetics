from django.shortcuts import render, redirect, get_object_or_404
from apps.baskets.models import Basket, BasketItem
from apps.products.models import Product
from apps.baskets.helper import get_client_ip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def basket_list_view(request):
    ip_address = get_client_ip(request)

    basket, _ = Basket.objects.get_or_create(
        user_ip=ip_address,
        is_active=True
    )

    context = {
        "basket": basket
    }
    return render(request, "baskets/list.html", context)


@csrf_exempt
def basket_create_view(request):
    ip_address = get_client_ip(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    quantity = data.get("quantity")

    if quantity < 1:
        return JsonResponse({"message": "Quantity can't be below than zero", "success": False}, status=400)

    basket, _ = Basket.objects.get_or_create(
        user_ip=ip_address, is_active=True
    )

    basket_item, created = BasketItem.objects.get_or_create(
        basket=basket, product=product, defaults={"quantity": quantity}
    )
    if not created:
        basket_item.quantity += quantity
        basket_item.save()

    return JsonResponse(
    {
            "basket_item": basket_item.id,
            "quantity": basket_item.quantity,
            "success": True,
            "product_total_price": f"{basket_item.total_price:.2f}",
            "total_price": f"{basket.total_price:.2f}"
        },
        status=201
    )


@csrf_exempt
def basket_delete_view(request):
    ip_address = get_client_ip(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")
    product = get_object_or_404(Product, id=product_id)
    quantity = data.get("quantity")

    if quantity < 1:
        return JsonResponse({"message": "Quantity can't be below than zero", "success": False}, status=400)

    try:
        basket = Basket.objects.get(
            user_ip=ip_address, is_active=True
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)}, status=400
        )

    try:
        basket_item = BasketItem.objects.get(
            basket=basket, product=product
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)}, status=400
        )

    if quantity > basket_item.quantity:
        return JsonResponse({"message": "Quantity must be below than quantity in basket"})


    basket_item.quantity -= quantity
    basket_item.save()

    quantity = basket_item.quantity
    id = basket_item.id

    if basket_item.quantity == 0:
        basket_item.delete()

    return JsonResponse(
        {
            "basket_item": id,
            "quantity": quantity,
            "success": True,
            "product_total_price": f"{basket_item.total_price:.2f}",
            "total_price": f"{basket.total_price:.2f}"
        },
        status=201
    )


@csrf_exempt
def basket_remove_view(request):
    ip_address = get_client_ip(request)
    data = json.loads(request.body)
    product_id = data.get("product_id")
    product = get_object_or_404(Product, id=product_id)

    try:
        basket = Basket.objects.get(
            user_ip=ip_address, is_active=True
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)}, status=400
        )

    try:
        basket_item = BasketItem.objects.get(
            basket=basket, product=product
        )
    except Exception as e:
        return JsonResponse(
            {"message": str(e)}, status=400
        )

    basket_item.delete()

    return JsonResponse(
        {"success": True, "total_price": f"{basket.total_price:.2f}"}, status=201
    )