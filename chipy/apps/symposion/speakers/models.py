import datetime

from django.db import models
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from markitup.fields import MarkupField


class Speaker(models.Model):
    
    SESSION_COUNT_CHOICES = [
        (1, "One"),
        (2, "Two")
    ]
    
    user = models.OneToOneField(User, null=True, related_name="speaker_profile")
    name = models.CharField(max_length=100)
    biography = MarkupField(help_text="A little bit about you. Edit using <a href='http://warpedvisions.org/projects/markdown-cheat-sheet/' target='_blank'>Markdown</a>.")
    photo = models.ImageField(upload_to="speaker_photos", blank=True)
    twitter_username = models.CharField(
        max_length = 15,
        blank = True,
        help_text = "Your Twitter account, with or without the @"
    )
    annotation = models.TextField() # staff only
    invite_email = models.CharField(max_length=200, unique=True, null=True, db_index=True)
    invite_token = models.CharField(max_length=40, db_index=True)
    created = models.DateTimeField(
        default = datetime.datetime.now,
        editable = False
    )
    sessions_preference = models.IntegerField(
        choices=SESSION_COUNT_CHOICES,
        null=True,
        blank=True,
        help_text="If you've submitted multiple proposals, please let us know if you only want to give one or if you'd like to give two talks. You may submit more than two proposals."
    )
    
    def __unicode__(self):
        if self.user:
            return self.name
        else:
            return "?"
    
    def get_absolute_url(self):
        return reverse("speaker_edit")
    
    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        else:
            return self.invite_email
