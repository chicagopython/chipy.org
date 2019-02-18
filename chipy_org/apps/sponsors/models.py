from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse


class MeetingSponsor(models.Model):
    sponsor = models.ForeignKey("sponsors.Sponsor")
    meeting = models.ForeignKey("meetings.Meeting", related_name="meeting_sponsors")
    about = models.TextField(u"About this sponsorship", blank=True, null=True)
    about_short = models.CharField(
        "Brief description of sponsorship",
        max_length=128, blank=True, null=True)

    def __str__(self):
        return "{name} sponsored {meeting}".format(
            name=self.sponsor.name,
            meeting=self.meeting)

    class Meta:
        verbose_name = "Meeting Sponsor"
        verbose_name_plural = "Meeting Sponsors"
        ordering = ["sponsor__name"]


class GeneralSponsor(models.Model):
    sponsor = models.ForeignKey("sponsors.Sponsor")
    about = models.TextField(u"About this sponsorship", blank=True, null=True)
    about_short = models.CharField(
        "Brief description of sponsorship",
        max_length=128, blank=True, null=True)

    def __str__(self):
        return "{name} sponsored".format(
            name=self.sponsor.name)

    class Meta:
        verbose_name = "General Sponsor"
        verbose_name_plural = "General Sponsors"
        ordering = ["sponsor__name"]


class Sponsor(models.Model):

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="sponsor_logos", blank=True, null=True,
        help_text=("All logos will be cropped to fit a 4 by 3 aspect ratio. "
                   "Resolution should be at minimum 400x300."))

    def __str__(self):
        return "{name}".format(name=self.name)

    def get_absolute_url(self):
        return reverse("sponsor_detail", args=[self.slug])
