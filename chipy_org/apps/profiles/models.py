from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    display_name = models.CharField(max_length=200, verbose_name="Name for Security Check In")
    show = models.BooleanField(default=False, verbose_name="Show my information in the member list")
    is_external_recruiter = models.BooleanField(
        default=False, verbose_name="Are you an external recruiter?"
    )


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance, display_name=instance.get_full_name())
