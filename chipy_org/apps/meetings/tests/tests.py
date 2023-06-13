# pylint: disable=invalid-name,no-member,unused-variable,duplicate-code
import datetime

import pytest
from django.conf import global_settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .. import email
from ..models import Meeting, MeetingType, Presenter, Topic, Venue

User = get_user_model()

pytestmark = pytest.mark.django_db


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username="chipy",
        )
        self.meeting = Meeting.objects.create(
            when=datetime.datetime.now() + datetime.timedelta(days=7),
            in_person_capacity=5,
        )
        self.topic = Topic.objects.create(title="test topic")

    def test__past_meetings__GET(self):
        # TEST
        response = self.client.get(reverse("past_meetings"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__meeting_detail__GET(self):
        # TEST
        response = self.client.get(reverse("meeting", args=[self.meeting.id]), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__propose_topic__GET__annon(self):
        # TEST
        response = self.client.get(reverse("propose_topic"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__propose_topic__GET__auth(self):
        # SETUP
        self.client.force_login(self.user)

        # TEST
        response = self.client.get(reverse("propose_topic"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__past_topics__GET(self):
        # TEST
        response = self.client.get(reverse("past_topics"), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)

    def test__past_topic__GET(self):
        # TEST
        response = self.client.get(reverse("past_topic", args=[self.topic.id]), follow=True)

        # CHECK
        self.assertEqual(response.status_code, 200)


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_future_meetings(client):
    test_venue = Venue.objects.create(name="Test")
    upcoming_meeting, _ = Meeting.objects.get_or_create(
        when=datetime.date.today() + datetime.timedelta(days=1),
        where=test_venue,
        key="some_upcoming_meeting",
        in_person_capacity=5,
    )
    past_meeting, _ = Meeting.objects.get_or_create(
        when=datetime.date.today() - datetime.timedelta(days=1),
        where=test_venue,
        key="some_past_meeting",
        in_person_capacity=5,
    )
    response = client.get(reverse("future_meetings"))
    assert response.status_code == 200


class MeetingTitleTest(TestCase):
    # Tests if 'custom_title' from 'meeting' is available, it'll be used as
    # 'title' for meeting.  If 'custom_title' from 'meeting' isn't available,
    # the 'default_title' from 'meeting_type' will be used as 'title' for
    # meeting.

    def setUp(self):
        self.meeting_type_non_main = MeetingType.objects.create(
            name="Non Main Sig ",
            default_title="Non Main Default Title",
        )

    def test_non_main_meeting_without_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(),
            meeting_type=self.meeting_type_non_main,
            in_person_capacity=5,
        )
        self.assertEqual(meeting.title, "Non Main Default Title")

    def test_main_meeting_without_custom_field(self):
        meeting = Meeting.objects.create(when=datetime.date.today(), in_person_capacity=5)
        self.assertEqual(meeting.title, "ChiPy __Main__ Meeting")

    def test_non_main_meeting_with_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(),
            meeting_type=self.meeting_type_non_main,
            custom_title="Non Main Custom Title",
            in_person_capacity=5,
        )
        self.assertEqual(meeting.title, "Non Main Custom Title")

    def test_main_meeting_with_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(),
            custom_title="Main Custom Title",
            in_person_capacity=5,
        )
        self.assertEqual(meeting.title, "Main Custom Title")


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_my_talks_with_multiple_presenters_with_same_user(client):
    user = User.objects.create(
        username="chipy",
    )

    p1 = Presenter.objects.create(
        user=user,
        name="name1",
    )
    t1 = Topic.objects.create(title="title1")
    t1.presenters.set(
        [
            p1,
        ]
    )

    p2 = Presenter.objects.create(
        user=user,
        name="name2",
    )
    t2 = Topic.objects.create(title="title2")
    t2.presenters.set(
        [
            p2,
        ]
    )

    client.force_login(user)
    response = client.get(reverse("my_topics"))

    assert response.status_code == 200
