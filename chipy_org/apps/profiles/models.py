from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    class Role(models.TextChoices):
        MEMBER = "MEMBER", "Member"
        ORGANIZER = "ORGANIZER", "Organizer"
        BOARD = "BOARD", "Board Member"
        SECRETARY = "SECRETARY", "Secretary"
        TREASURER = "TREASURER", "Treasurer"
        CHAIR = "CHAIR", "Chair"

        @classmethod
        def officer_roles(cls):
            return [cls.SECRETARY, cls.TREASURER, cls.CHAIR]

        @classmethod
        def board_roles(cls):
            return [cls.BOARD] + cls.officer_roles()

        @classmethod
        def organizer_roles(cls):
            return [cls.ORGANIZER] + cls.board_roles()

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=200, verbose_name="Name for Security Check In")
    show = models.BooleanField(default=False, verbose_name="Show my information in the member list")
    role = models.CharField(
        max_length=16, choices=Role.choices, default=Role.MEMBER, verbose_name="Organizational role"
    )
    bio = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Short bio that will appear on organizer page",
    )
    public_email = models.EmailField(
        max_length=64, null=True, blank=True, verbose_name="Email that will be displayed publicly"
    )
    public_website = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name="Website that will be displayed publicly",
    )

    @classmethod
    def user_organizers(cls):
        return User.objects.filter(profile__role__in=cls.Role.organizer_roles())

    @property
    def is_officer(self):
        return self.role in UserProfile.Role.officer_roles()

    @property
    def is_board_member(self):
        return self.role in UserProfile.Role.board_roles()

    @property
    def is_organizer(self):
        return self.role in UserProfile.Role.organizer_roles()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        UserProfile.objects.get_or_create(user=instance, display_name=instance.get_full_name())
