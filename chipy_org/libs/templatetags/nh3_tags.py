import logging
from typing import Any

import nh3
from django import template
from django.conf import settings
from django.utils.safestring import SafeText, mark_safe

logger = logging.getLogger(__name__)
register = template.Library()


def get_nh3_default_options() -> dict[str, Any]:
    """
    Pull the nh3 settings similarly to how django-bleach handled them.
    Further customization is possible, see https://nh3.readthedocs.io/en/latest/#module-nh3.

    Some django-bleach settings can be mapped to nh3 settings without
    any changes:

        BLEACH_ALLOWED_TAGS         -> NH3_ALLOWED_TAGS
        BLEACH_ALLOWED_ATTRIBUTES   -> NH3_ALLOWED_ATTRIBUTES
        BLEACH_STRIP_COMMENTS       -> NH3_STRIP_COMMENTS
        BLEACH_ALLOWED_PROTOCOLS    -> NH3_ALLOWED_URL_SCHEMES
        BLEACH_STRIP_TAGS           -> This is the default behavior of nh3

    While other settings are have no current support in nh3:

        BLEACH_ALLOWED_STYLES       -> There is no support for styling

    """
    nh3_args: dict[str, Any] = {}

    nh3_settings = {
        "NH3_ALLOWED_TAGS": "tags",
        "NH3_ALLOWED_ATTRIBUTES": "generic_attribute_prefixes",
        "NH3_STRIP_COMMENTS": "strip_comments",
        "NH3_ALLOWED_URL_SCHEMES": "url_schemes",
    }

    for setting, kwarg in nh3_settings.items():
        if hasattr(settings, setting):
            attr = getattr(settings, setting)

            # Convert from general iterables to sets
            if setting == "NH3_ALLOWED_TAGS":
                attr = set(attr)
            if setting == "NH3_ALLOWED_URL_SCHEMES":
                attr = set(attr)
            if setting == "NH3_ALLOWED_ATTRIBUTES":
                attr = set(attr)

            nh3_args[kwarg] = attr

    return nh3_args


@register.filter(name="nh3")
def nh3_value(value: str | None, tags: str | None = None) -> SafeText | None:
    """
    Takes an input HTML value and sanitizes it utilizing nh3,
        returning a SafeText object that can be rendered by Django.

    Accepts an optional argument of allowed tags. Should be a comma delimited
        string (i.e. "img,span" or "img")
    """
    if value is None:
        return None

    nh3_args = get_nh3_default_options()
    if tags is not None:
        args = nh3_args.copy()
        args["tags"] = set(tags.split(","))
    else:
        args = nh3_args

    clean_value = nh3.clean(value, **args)
    return mark_safe(clean_value)
