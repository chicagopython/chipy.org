from django.contrib.flatpages.models import FlatPage
from django.db import models


class CustomFlatPage(FlatPage):
    header_image = models.ImageField(
        upload_to="flatpage_headers/",
        blank=True,
        null=True,
        help_text="Custom header image for the flat page.",
    )

    class Meta:
        verbose_name = "Custom Flat Page"
        verbose_name_plural = "Custom Flat Pages"
