# pylint: disable=invalid-name, duplicate-code, redefined-outer-name
import pytest
from django.conf import global_settings
from django.test import override_settings
from django.urls import reverse

from .models import Sponsor

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def with_static_files():
    with override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE):
        yield


@pytest.fixture
def sponsor():
    return Sponsor.objects.create(slug="chipy", name="Chipy")


@pytest.fixture
def sponsor_with_logo():
    return Sponsor.objects.create(
        name="test-name",
        slug="test-slug",
        url="test-url",
        description="test-description",
        logo="./test-resources/deadpool.jpg",
    )


def test_sponsor_list(client, sponsor):
    url = reverse("sponsor_list")
    response = client.get(url, follow=True)
    assert response.status_code == 200


def test_sponsor_detail(client, sponsor):
    response = client.get(reverse("sponsor_detail", args=[sponsor.slug]), follow=True)
    assert response.status_code == 200


def test_sponsor_detail_logo(client, sponsor_with_logo):
    response = client.get(reverse("sponsor_detail", args=[sponsor_with_logo.slug]), follow=True)
    assert response.status_code == 200

    html = str(response.content)
    assert sponsor_with_logo.name in html
    assert sponsor_with_logo.url in html
    assert sponsor_with_logo.description in html
    assert "img" in html
