from __future__ import unicode_literals
import time

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


class SponsorGroup(models.Model):
    name = models.CharField(max_length=80)
    list_priority = models.IntegerField(default=5)
    featured_sponsor_weight = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("list_priority",)


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

    @property
    def featured_sponsor_weight(self):
        return self.sponsor_group.featured_sponsor_weight

    def get_absolute_url(self):
        return reverse("sponsor_detail", args=[self.slug])

    @classmethod
    def featured_sponsor(cls, second_shift_constant=10):
        """
        Return a featured sponsor based on the current time, the sponsor levels, and a
        bit shift constant that determines length of overall cycle

          second_shift_constant is the amount seconds will be bitshifted by when
          calculating the featured sponsor. If set to 0, the cycle of all sponsors
          will complete in 100 seconds. If set to 1, it will be 200 seconds, 2 is
          400 seconds, and 12 is 409600 or 4.75 days.
        """
        sponsors = cls.objects.select_related("sponsor_group").all()

        current_time_mod = (int(time.time()) >> second_shift_constant) % 100  # eg 36

        total_number_of_chunks = sum(s.featured_sponsor_weight for s in sponsors)
        if total_number_of_chunks == 0:
            return

        chunk_size = 100 / total_number_of_chunks
        chunk_end = 0
        for sponsor in sponsors:
            chunk_end = chunk_end + sponsor.featured_sponsor_weight * chunk_size
            if current_time_mod < chunk_end:
                return sponsor

    class Meta:
        ordering = ["name"]
