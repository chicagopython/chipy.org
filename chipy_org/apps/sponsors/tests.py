# pylint: disable=invalid-name, duplicate-code, redefined-outer-name
from django.core.urlresolvers import reverse
from django.conf import global_settings
from django.test import override_settings, Client
import pytest

from .models import Sponsor


pytestmark = pytest.mark.django_db


@pytest.fixture
def sponsor():
    return Sponsor.objects.create(slug="chipy", name="Chipy")


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def sponsor_with_logo():
    return Sponsor.objects.create(
        name="test-name",
        slug="test-slug",
        url="test-url",
        description="test-description",
        logo="./test-resources/deadpool.jpg",
    )


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_sponsor_list(client, sponsor):
    response = client.get(reverse("sponsor_list"))
    assert response.status_code == 200


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_sponsor_detail(client, sponsor):
    response = client.get(reverse("sponsor_detail", args=[sponsor.slug]), follow=True)
    assert response.status_code == 200


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_sponsor_detail_logo(client, sponsor_with_logo):
    response = client.get(
        reverse("sponsor_detail", args=[sponsor_with_logo.slug]), follow=True
    )
    assert response.status_code == 200

    html = str(response.content)
    assert sponsor_with_logo.name in html
    assert sponsor_with_logo.url in html
    assert sponsor_with_logo.description in html
    assert "img" in html
