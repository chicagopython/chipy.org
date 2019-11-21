# pylint: disable=invalid-name,duplicate-code
import pytest
from django.test import TestCase, override_settings, Client
from django.core.urlresolvers import reverse
from django.conf import global_settings
from django.contrib.auth import get_user_model
from .models import Sponsor

pytestmark = pytest.mark.django_db

User = get_user_model()


@override_settings(
    STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="chipy",)
        self.sponsor = Sponsor.objects.create(
            slug="chipy",
            name="Chipy"
        )

    def test__sponsor_detail__GET(self):
        # SETUP

        # TEST
        response = self.client.get(
            reverse('sponsor_detail', args=[self.sponsor.slug]), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__sponsor_list__GET(self):
        # SETUP

        # TEST
        response = self.client.get(
            reverse('sponsor_list'), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)
