import pytest
from django.contrib.auth.models import User

from ..models import UserProfile

pytestmark = pytest.mark.django_db


def test_profile_has_role_attribute():
    user = User.objects.create()

    user.profile.role = UserProfile.Role.ORGANIZER
    user.profile.save()

    profile = UserProfile.objects.get(user=user)
    assert profile.is_organizer
    assert not profile.is_board_member
    assert not profile.is_officer

    profile.role = UserProfile.Role.BOARD
    assert profile.is_organizer
    assert profile.is_board_member
    assert not profile.is_officer

    profile.role = UserProfile.Role.TREASURER
    assert profile.is_organizer
    assert profile.is_board_member
    assert profile.is_officer
