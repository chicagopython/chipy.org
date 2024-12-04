from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from chipy_org.libs.models import CommonModel


class AnnouncementQuerySet(models.QuerySet):
    def active(self):
        now = timezone.now()
        return (
            self.filter(active=True)
            .filter(models.Q(end_date__isnull=True) | models.Q(end_date__gte=now))
            .order_by("created")
        )

    def featured(self):
        try:
            feature = self.active().latest("created")
        except Announcement.DoesNotExist:
            feature = None
        return feature


class Announcement(CommonModel):
    headline = models.TextField(max_length="100")
    text = models.TextField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active = models.BooleanField(
        default=True, help_text="Has this announcement been published yet?"
    )
    photo = models.ImageField(upload_to="announcements", blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    objects = AnnouncementQuerySet.as_manager()

    def __str__(self):
        return f"{self.id}: {self.headline}"
