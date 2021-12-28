# pylint: disable=invalid-name,duplicate-code
import pytest
from django.conf import global_settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse

User = get_user_model()


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="chipy",
        )

    def test__profile_list_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse("profiles:list"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__profile_edit_url__GET_annon(self):
        # SETUP

        # TEST
        response = self.client.get(reverse("profiles:edit"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__profile_edit_url__GET_auth(self):
        # SETUP
        self.client.force_login(self.user)

        # TEST
        response = self.client.get(reverse("profiles:edit"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    @pytest.mark.skip(
        reason="Redirect codes are getting jumbled because"
        "301s are redirecting to https in ci"
        "and 302s are what we want to test"
    )
    def test__profile_edit_url__POST_auth(self):
        # SETUP
        display_name = "ChiPy"
        self.client.force_login(self.user)

        # TEST
        response = self.client.post(
            reverse("profiles:edit"), {"display_name": display_name, "show": True}, follow=False
        )

        # CHECK
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.profile.display_name, display_name)
        self.assertTrue(self.user.profile.show)
