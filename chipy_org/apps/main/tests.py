# pylint: disable=invalid-name,duplicate-code
import pytest
from django.test import TestCase, override_settings
from django.test import Client
from django.core.urlresolvers import reverse_lazy
from django.conf import global_settings

pytestmark = pytest.mark.django_db


@override_settings(
    STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test__home_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse_lazy('home'), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)


@pytest.mark.parametrize(
    'test_in, result', [
        (True, True),
        (False, False),
        ('t', True),
        ('f', False),
        ('true', True),
        ('false', False),
        ('1', '1'),
        (1, '1'),
        ('foo', 'foo'),
    ]
)
def test_settingspy_env_var(monkeypatch, test_in, result):
    monkeypatch.setenv('TEST_VAR', test_in)
    from chipy_org import settings
    assert settings.env_var('TEST_VAR') == result


@pytest.mark.parametrize(
    'test_in, result', [
        ('', []),
        ('f@e.com', ["f@e.com"]),
        ('f@e.com,b@e.com', ["f@e.com", "b@e.com"]),
    ]
)
def test_settingspy_env_list(monkeypatch, test_in, result):
    monkeypatch.setenv('TEST_VAR', test_in)
    from chipy_org import settings
    assert settings.env_list('TEST_VAR') == result
