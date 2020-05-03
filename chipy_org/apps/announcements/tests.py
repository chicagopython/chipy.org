# pylint: disable=invalid-name,duplicate-code
import pytest
from django.conf import global_settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

pytestmark = pytest.mark.django_db


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test__announcements_list_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse("announcements_list"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)
