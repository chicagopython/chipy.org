from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


@python_2_unicode_compatible
class MeetingSponsor(models.Model):
    sponsor = models.ForeignKey("sponsors.Sponsor")
    meeting = models.ForeignKey("meetings.Meeting")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return "{name} sponsored {meeting}".format(
            name=self.sponsor.name,
            meeting=self.meeting)

    class Meta:
        verbose_name = "Meeting Sponsor"
        verbose_name_plural = "Meeting Sponsors"


@python_2_unicode_compatible
class Sponsor(models.Model):

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="sponsor_logos", blank=True, null=True)
    
    def __str__(self):
        return "{name}".format(name=self.name)

