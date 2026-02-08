# core/middleware.py
from django.utils import translation

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.COOKIES.get('django_language'):
            translation.activate('az')
            request.LANGUAGE_CODE = 'az'
        return self.get_response(request)
