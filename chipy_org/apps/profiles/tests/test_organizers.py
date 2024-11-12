import pytest
from django.conf import global_settings
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from ..models import UserProfile

pytestmark = pytest.mark.django_db


def test_organizers_page_displayed(client):
    public_information = {
        "bio": "Wild for acorns",
        "display_name": "John Smith",
        "public_email": "secretsquirrel@example.com",
        "public_website": "https://johns-favorite-acorns.example.com",
    }
    user = User.objects.create()
    UserProfile.objects.filter(user=user).update(
        role=UserProfile.Role.ORGANIZER, **public_information
    )

    response = client.get(reverse("profiles:organizers"))
    assert response.status_code == 200
    stringified_content = str(response.content)
    for value in public_information.values():
        assert value in stringified_content


def test_organizers_non_organizer_show_up_incorrectly(client):
    User.objects.create(first_name="Paul", last_name="Blart")
    response = client.get(reverse("profiles:organizers"))
    assert response.status_code == 200
    assert "Paul Blart" not in str(response.content)
