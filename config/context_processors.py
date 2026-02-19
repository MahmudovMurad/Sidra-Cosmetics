from django.core.cache import cache
from apps.baskets.models import Basket
from apps.baskets.helper import get_client_ip
from apps.mainapp.models import Settings, Banner


def extras(request):
    ip_address = get_client_ip(request)

    # Cache Settings singleton — avoid DB hit on every request
    settings = cache.get('site_settings')
    if settings is None:
        settings = Settings.get_solo()
        if settings:
            cache.set('site_settings', settings, 300)  # 5 minutes

    # Basket lookup — use only('id') since we just need the count
    basket = Basket.objects.filter(
        is_active=True, user_ip=ip_address
    ).only('id').first()

    # Cache banners — rarely change, no need to query every request
    banners = cache.get('site_banners')
    if banners is None:
        banners = list(Banner.objects.all())
        cache.set('site_banners', banners, 300)  # 5 minutes

    return {
        "cart_count": basket.basketitem_set.count() if basket else 0,
        "settings": settings,
        "banners": banners,
    }