# pylint: disable=unused-wildcard-import,wildcard-import
from .settings import *

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:", "TEST": {}}}
DEBUG = True
ADMINS = "admin@chipy.org"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ENVELOPE_EMAIL_RECIPIENTS = "admin@example.com"

SECRET_KEY = "somesecretkeyfordjangogoeshere"

USE_S3 = False

NORECAPTCHA_SITE_KEY = "dummy_recaptcha_public_key"
NORECAPTCHA_SECRET_KEY = "dummy_recaptcha_private_key"
