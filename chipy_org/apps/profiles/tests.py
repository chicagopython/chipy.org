# pylint: disable=invalid-name,duplicate-code
import pytest
import django
from django.test import TestCase, override_settings
from django.test import Client
from django.core.urlresolvers import reverse_lazy
from django.conf import global_settings
from django.contrib.auth import get_user_model


User = get_user_model()


@override_settings(
    STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="chipy",)

    def test__profile_list_url__GET(self):
        # SETUP

        # TEST
        response = self.client.get(reverse_lazy('profiles:list'), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__profile_edit_url__GET_annon(self):
        # SETUP

        # TEST
        response = self.client.get(reverse_lazy('profiles:edit'), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 302)

    @pytest.mark.skipif(
        django.VERSION < (1, 9, 0),
        reason="Django 1.9 introduces force_login")
    def test__profile_edit_url__GET_auth(self):
        # SETUP
        self.client.force_login(self.user)

        # TEST
        response = self.client.get(reverse_lazy('profiles:edit'), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    @pytest.mark.skipif(
        django.VERSION < (1, 9, 0),
        reason="Django 1.9 introduces force_login")
    def test__profile_edit_url__POST_auth(self):
        # SETUP
        display_name = "ChiPy"
        self.client.force_login(self.user)

        # TEST
        response = self.client.post(
            reverse_lazy('profiles:edit'),
            {'display_name': display_name, 'show': True}, follow=True)

        # CHECK
        self.user.profile.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.user.profile.display_name,
            display_name)
        self.assertTrue(self.user.profile.show)
