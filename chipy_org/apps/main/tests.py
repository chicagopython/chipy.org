# pylint: disable=invalid-name,duplicate-code
import pytest
from django.conf import global_settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


@override_settings(STORAGES=global_settings.STORAGES)
class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test__home_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse("home"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)


@pytest.mark.parametrize(
    "test_in, result",
    [
        ("t", True),
        ("f", False),
        ("true", True),
        ("false", False),
        ("1", "1"),
        ("foo", "foo"),
    ],
)
def test_settingspy_env_var(monkeypatch, test_in, result):
    monkeypatch.setenv("TEST_VAR", test_in)
    from chipy_org import settings  # pylint: disable=import-outside-toplevel

    assert settings.env_var("TEST_VAR") == result


@pytest.mark.parametrize(
    "test_in, result",
    [
        ("", []),
        ("f@e.com", ["f@e.com"]),
        ("f@e.com,b@e.com", ["f@e.com", "b@e.com"]),
    ],
)
def test_settingspy_env_list(monkeypatch, test_in, result):
    monkeypatch.setenv("TEST_VAR", test_in)
    from chipy_org import settings  # pylint: disable=import-outside-toplevel

    assert settings.env_list("TEST_VAR") == result


def test_logout_redirects_to_home(client):
    response = client.post("/logout/", follow=True)
    assert response.status_code == 200
    assert response.request["PATH_INFO"] == "/"
