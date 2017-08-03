from django.test import TestCase, override_settings
from django.test import Client
from django.core.urlresolvers import reverse_lazy
from django.conf import global_settings
from django.contrib.auth import get_user_model
from .models import SubGroup


User = get_user_model()


@override_settings(
    STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="chipy",)
        self.group = SubGroup.objects.create(
            name="test_group", slug="test_group")

    def test__sponsor_detail__GET(self):
        # SETUP

        # TEST
        response = self.client.get(
            reverse_lazy('groups', args=[self.group.slug]))

        # CHECK
        self.assertEqual(response.status_code, 200)
