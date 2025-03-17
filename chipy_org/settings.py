# -*- coding: utf-8 -*-
# Django settings for account project

import os
from pathlib import Path
from warnings import filterwarnings

import dj_database_url


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if isinstance(val, str):
        lower_val = val.lower()
        if lower_val in ["t", "true"]:
            val = True
        elif lower_val in ["f", "false"]:
            val = False
    return val


def env_list(key, defaults=None, delimiter=","):
    if not defaults:
        defaults = []
    val_list = defaults
    val = os.environ.get(key, None)
    if val:
        val_list = val.split(delimiter)
    return val_list


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = env_var("DEBUG", False)

ALLOWED_HOSTS = [
    "chipy.org",
    "www.chipy.org",
    "chipy.herokuapp.com",
    "chipy-149.herokuapp.com",
    "localhost:8000",
    "localhost",
    "www.localhost:8000",
    "www.localhost",
]

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", ALLOWED_HOSTS)


# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = env_var("SERVE_MEDIA", DEBUG)

SECURE_SSL_REDIRECT = env_var("SECURE_SSL_REDIRECT", True)

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [(admin.split("@")[0], admin) for admin in env_var("ADMINS", "").split(",")]


MANAGERS = ADMINS


BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CHIPY_BACKUP_TALK_REVIEWERS = env_list("CHIPY_BACKUP_TALK_REVIEWERS")

CHIPY_TOPIC_SUBMIT_EMAILS = env_var("CHIPY_TOPIC_SUBMIT_EMAILS", "").split(",")

CHICAGO_ORGANIZER_EMAILS = env_var("CHICAGO_ORGANIZER_EMAILS", "").split(",")

# dj_database_url will pull from the DATABASE_URL environment variable
DATABASES = {"default": dj_database_url.config(default="postgres://localhost:5432/chipy_org")}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:", "TEST": {}}}
DDEBUG = True
ADMINS = ["admin@chipy.org"]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ENVELOPE_EMAIL_RECIPIENTS = [
    "admin@example.com",
]



SECRET_KEY = "somesecretkeyfordjangogoeshere"
SECURE_SSL_REDIRECT = False

NORECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
NORECAPTCHA_SECRET_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

CAPTCHA_TEST_MODE = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = env_var("SITE_ID", 1)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

USE_S3 = env_var("USE_S3", False)

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_QUERYSTRING_AUTH = False
    AWS_HEADERS = {
        "Cache-Control": "max-age=86400",
    }
    # STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    # these next two aren't used, but staticfiles will complain without them
    # STATIC_URL = f"https://{os.environ['AWS_STORAGE_BUCKET_NAME']}.s3.amazonaws.com/static/"
else:
    MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "mediafiles"))


JOB_POST_KEY = env_var("JOB_POST_KEY", "")


STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "staticfiles"))

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = env_var("SECRET_KEY")

ROOT_URLCONF = "chipy_org.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_ROOT, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.login_redirect",
            ],
            "loaders": [
                "admin_tools.template_loaders.Loader",
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    },
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "chipy_org.libs.middleware.ChipySocialAuthExceptionMiddleware",  # social auth settings
]

# Start of Python Social Auth settings
SOCIAL_AUTH_GITHUB_KEY = env_var("GITHUB_APP_ID")
SOCIAL_AUTH_GITHUB_SECRET = env_var("GITHUB_API_SECRET")

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env_var("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env_var("GOOGLE_OAUTH2_CLIENT_SECRET")

LOGIN_URL = "/login/"
LOGIN_ERROR_URL = "/"
LOGIN_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    "social_core.backends.twitter.TwitterOAuth",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
    "social_core.backends.open_id.OpenIdAuth",
    "django.contrib.auth.backends.ModelBackend",
]

SOCIAL_AUTH_ENABLED_BACKENDS = (
    "google",
    "github",
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

SOCIAL_AUTH_PROTECTED_USER_FIELDS = [
    "email",
]

GITHUB_EXTRA_DATA = [
    ("email", "email"),
]
# End of Python Social Auth Settings

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"

INSTALLED_APPS = [
    # Admin Tools
    "admin_tools",
    "admin_tools.theming",
    "admin_tools.menu",
    "admin_tools.dashboard",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
    # Third party
    "django_gravatar",
    "django_ical",
    "django_recaptcha",
    "custom_flatpages",
    "flatblocks",
    "gunicorn",
    "honeypot",
    "rest_framework",
    "social_django",
    "sorl.thumbnail",
    "storages",
    "tinymce",
    # theme
    "crispy_forms",
    "crispy_bootstrap5",
    # project
    "chipy_org.apps.main",
    "chipy_org.apps.announcements",
    "chipy_org.apps.contact",
    "chipy_org.apps.job_board",
    "chipy_org.apps.meetings",
    "chipy_org.apps.profiles",
    "chipy_org.apps.sponsors",
    "chipy_org.apps.subgroups",
    "chipy_org.apps.talks",
    "chipy_org.libs",
    #Poll.config 
    'polls',
]
if DEBUG:
    INSTALLED_APPS.append("chipy_org.dev_utils")

TEST_RUNNER = "chipy_org.runner.PytestTestRunner"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_FAIL_SILENTLY = not DEBUG
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

if DEBUG:
    # Add the command extensions
    INSTALLED_APPS += ["django_extensions"]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ENVELOPE_EMAIL_RECIPIENTS = env_var("ENVELOPE_EMAIL_RECIPIENTS", "").split(",")

EMAIL_BACKEND = env_var("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env_var("EMAIL_HOST", "smtp.sendgrid.net")
EMAIL_HOST_USER = env_var("EMAIL_HOST_USER", env_var("SENDGRID_USERNAME", None))
EMAIL_HOST_PASSWORD = env_var("EMAIL_HOST_PASSWORD", env_var("SENDGRID_PASSWORD", None))
EMAIL_PORT = int(env_var("EMAIL_PORT", 587))
EMAIL_USE_TLS = env_var("EMAIL_USE_TLS", True)

DEFAULT_FROM_EMAIL = env_var("DEFAULT_FROM_EMAIL", "DoNotReply@chipy.org")
HONEYPOT_FIELD_NAME = "email2"

if env_var("PRODUCTION", False):
    PREPEND_WWW = True

NH3_ALLOWED_TAGS = [
    "p",
    "b",
    "i",
    "u",
    "em",
    "code",
    "strong",
    "a",
    "span",
    "tt",
    "hr",
    "img",
    "abbr",
    "sub",
    "sup",
    "table",
    "tbody",
    "tr",
    "td",
    "th",
    "br",
    "li",
    "pre",
    "strong",
    "ul",
    "h1",
    "h2",
    "h3",
    "div",
    "iframe",
    "src",
    "class",
]
NH3_ALLOWED_ATTRIBUTES = ["href", "title", "style", "rel", "img", "src", "alt"]
NH3_ALLOWED_URL_SCHEMES = ["http", "https", "data"]
NH3_STRIP_COMMENTS = True  # default, listed here for documentation

RECAPTCHA_PUBLIC_KEY = env_var("NORECAPTCHA_SITE_KEY")
RECAPTCHA_PRIVATE_KEY = env_var("NORECAPTCHA_SECRET_KEY")

MEETUP_API_KEY = env_var("MEETUP_API_KEY")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "loggers": {
        "chipy_org": {
            "handlers": ["console"],
            "level": "INFO",
        }
    },
}

STORAGES = {
    "default": {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

SILENCED_SYSTEM_CHECKS = []
if DEBUG:
    SILENCED_SYSTEM_CHECKS += ["django_recaptcha.recaptcha_test_key_error"]

filterwarnings("ignore", "The FORMS_URLFIELD_ASSUME_HTTPS transitional setting is deprecated.")
FORMS_URLFIELD_ASSUME_HTTPS = True
