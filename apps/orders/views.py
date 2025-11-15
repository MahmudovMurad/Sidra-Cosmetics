from django.shortcuts import render, redirect
from apps.baskets.helper import get_client_ip
from apps.baskets.models import Basket
from apps.orders.forms import OrderForm
from apps.orders.models import OrderItem
from django.utils import translation
from apps.payments.akbank import akbank_payment_gateway

# Create your views here.


def order_create_view(request):
    ip_address = get_client_ip(request)
    lang = translation.get_language()
    basket, _ = Basket.objects.get_or_create(
        user_ip=ip_address,
        is_active=True
    )

    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid() and basket.basketitem_set.count() > 0:
            obj = form.save(commit=True)

            if lang == "az":
                obj.currency = "azn"
            else:
                obj.currency = "tl"

            obj.save()

            basket_items = basket.basketitem_set.all()
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=obj,
                        product=basket_item.product,
                        price=basket_item.product.total_price,
                        quantity=basket_item.quantity
                    ) for basket_item in basket_items
                ]
            )

            basket.delete()

            if obj.pay_choice == "cod":
                return redirect("/")

            elif obj.pay_choice == "akbank":
                pay_link = akbank_payment_gateway.create_link(order=obj)
                return redirect(pay_link)

            elif obj.pay_choice == "pasha":
                ...

            return redirect("/")

    context = {
        "form": form,
        "basket": basket
    }
    return render(request, "orders/create.html", context)