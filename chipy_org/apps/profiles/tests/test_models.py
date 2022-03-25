import pytest
from django.contrib.auth.models import User

from ..models import UserProfile

pytestmark = pytest.mark.django_db


def test_profile_has_organizer_attribute():
    user = User.objects.create()

    user.profile.is_organizer = True
    user.profile.save()

    profile = UserProfile.objects.get(user=user)

    assert profile.is_organizer
