from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from apps.payments.united import united_payment_gateway


def payment_success_view(request):
    return render(request, "payments/success.html", {})

def payment_failure_view(request):
    return render(request, "payments/failure.html", {})

@csrf_exempt
def callback_view(request):
    up = request.GET.get("up")
    result = united_payment_gateway.handle_checkout(data=up)
    if not result:
        return redirect("payments:failure")
    # If needed, handle unexpected methods
    return redirect("payments:success")