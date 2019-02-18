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

    def test__announcements_list_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse_lazy('announcements_list'))

        # CHECK
        self.assertEqual(response.status_code, 200)
