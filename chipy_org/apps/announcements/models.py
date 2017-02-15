from __future__ import unicode_literals

from django.db import models
from chipy_org.libs.models import CommonModel
from ckeditor.fields import RichTextField


class Announcement(CommonModel):
    headline = models.TextField(max_length="100")
    text = RichTextField(blank=True, null=True)
    active = models.BooleanField(
        default=True,
        help_text="Has this announcement been published yet?")
    photo = models.ImageField(upload_to="announcements", blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return "{}: {}".format(self.id, self.headline)
