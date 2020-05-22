# pylint: disable=unused-wildcard-import,wildcard-import
from .settings import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:", "TEST": {}}}
DEBUG = True
ADMINS = ["admin@chipy.org"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ENVELOPE_EMAIL_RECIPIENTS = "admin@example.com"

SECRET_KEY = "somesecretkeyfordjangogoeshere"
SECURE_SSL_REDIRECT = False

NORECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
NORECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
