"""
URL configuration for loyalty project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView

# Sitemap: /sitemap.xml (dil prefiksi olmadan)
urlpatterns = [
    path(
        "sitemap.xml",
        TemplateView.as_view(template_name="sitemap.xml", content_type="application/xml"),
    ),
]

# Base urlpatterns
urlpatterns += i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("apps.mainapp.urls")),
    path("products/", include("apps.products.urls")),
    path("baskets/", include("apps.baskets.urls")),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
