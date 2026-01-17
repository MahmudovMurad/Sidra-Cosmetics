from apps.baskets.models import Basket
from apps.baskets.helper import get_client_ip
from apps.mainapp.models import Settings, Banner


def extras(request):
    ip_address = get_client_ip(request)

    settings = Settings.get_solo()
    print(settings)

    basket = Basket.objects.filter(
            is_active=True, user_ip=ip_address
    ).first()
    return {
        "cart_count": basket.basketitem_set.count() if basket else 0,
        "settings": settings,
        "banners": Banner.objects.all()
    }