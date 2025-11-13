from django.shortcuts import render, redirect
from apps.baskets.helper import get_client_ip
from apps.baskets.models import Basket
from apps.orders.forms import OrderForm
from apps.orders.models import OrderItem

# Create your views here.


def order_create_view(request):
    ip_address = get_client_ip(request)
    basket, _ = Basket.objects.get_or_create(
        user_ip=ip_address,
        is_active=True
    )

    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST or None)
        if form.is_valid():
            obj = form.save()

            if obj.pay_choice == "cod":

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

                return redirect("/")

            return redirect("/")

    context = {
        "form": form,
        "basket": basket
    }
    return render(request, "orders/create.html", context)