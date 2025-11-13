"""Settings for local development environment with enabled debugging tools."""

from config.settings.base import *  # noqa: F403
from config.settings.base import env

DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

if USE_DOCKER:  # noqa: F405
    ALLOWED_HOSTS += ["0.0.0.0"]  # nosec B104


# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips

if USE_DOCKER:  # noqa: F405
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips]
    INTERNAL_IPS += ["127.0.0.1", "10.0.2.2"]
else:
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

# EMAIL
# ---------------------------------------------------------------------
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
# DEFAULT_FROM_EMAIL = "Loyalty <info@loyalty.com>"
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
# SERVER_EMAIL = "Loyalty <info@loyalty.com>"


# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "bulk.smtp.mailtrap.io"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = 'noreply@play10.az'
#
#
# # For test sending email
# EMAIL_SENDER = {
#     "BACKEND": "apps.utils.email.backends.EmailSender"
# }