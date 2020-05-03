from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


class MeetingSponsor(models.Model):
    sponsor = models.ForeignKey("sponsors.Sponsor", on_delete=models.CASCADE)
    meeting = models.ForeignKey(
        "meetings.Meeting", related_name="meeting_sponsors", on_delete=models.CASCADE
    )
    about = models.TextField("About this sponsorship", blank=True, null=True)
    about_short = models.CharField(
        "Brief description of sponsorship", max_length=128, blank=True, null=True
    )

    def __str__(self):
        return f"{self.sponsor.name} sponsored {self.meeting}"

    class Meta:
        verbose_name = "Meeting Sponsor"
        verbose_name_plural = "Meeting Sponsors"
        ordering = ["sponsor__name"]


class GeneralSponsor(models.Model):
    sponsor = models.ForeignKey("sponsors.Sponsor", on_delete=models.CASCADE)
    about = models.TextField("About this sponsorship", blank=True, null=True)
    about_short = models.CharField(
        "Brief description of sponsorship", max_length=128, blank=True, null=True
    )

    def __str__(self):
        return f"{self.sponsor.name} sponsored"

    class Meta:
        verbose_name = "General Sponsor"
        verbose_name_plural = "General Sponsors"
        ordering = ["sponsor__name"]


class SponsorGroup(models.Model):
    name = models.CharField(max_length=80)
    list_priority = models.IntegerField(default=5)

    def __str__(self):
        return self.name


class Sponsor(models.Model):

    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="sponsor_logos",
        blank=True,
        null=True,
        help_text=(
            "All logos will be cropped to fit a 4 by 3 aspect ratio. "
            "Resolution should be at minimum 400x300."
        ),
    )
    sponsor_group = models.ForeignKey(
        SponsorGroup, related_name="sponsors", blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("sponsor_detail", args=[self.slug])

    class Meta:
        ordering = ["name"]
