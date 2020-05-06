# pylint: disable=invalid-name,no-member,unused-variable,duplicate-code
import datetime
import pytest
from django.test import TestCase, override_settings
from django.test import Client
from django.core import mail
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import global_settings
from django.contrib.auth import get_user_model

import chipy_org.libs.test_utils as test_utils
from ..models import RSVP, Meeting, Venue, Topic, TopicDraft, MeetingType, Presentor
from .. import email

User = get_user_model()

pytestmark = pytest.mark.django_db


class MeetingsTest(test_utils.AuthenticatedTest):
    def test_unique_rsvp(self):
        """
        Tests the uniqueness constraints on the rsvp model
        """
        test_venue = Venue.objects.create(name="Test")
        meeting = Meeting.objects.create(when=datetime.date.today(), where=test_venue)
        rsvp = RSVP.objects.create(user=self.user, meeting=meeting, response="Y")

        with self.assertRaises(ValidationError):
            # RSVP needs to have a user or name
            rsvp_no_user = RSVP.objects.create(meeting=meeting, response="Y")

        with self.assertRaises(ValidationError):
            # This should already exist
            duplicate_rsvp = RSVP.objects.create(user=self.user, meeting=meeting, response="Y")

        with self.assertRaises(ValidationError):
            name_rsvp = RSVP.objects.create(
                name="Test Name", meeting=meeting, response="Y", email="dummy@example.com",
            )

            # Can't have two of the same name
            duplicate_name_rsvp = RSVP.objects.create(
                name="Test Name", meeting=meeting, response="Y", email="dummy@example.com",
            )


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
class SmokeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="chipy",)
        self.meeting = Meeting.objects.create(
            when=datetime.datetime.now() + datetime.timedelta(days=7)
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


def test_post_topic_sends_email():
    m = Meeting(
        when=datetime.datetime.now(), reg_close_date=datetime.datetime.now(), description="Test",
    )
    m.save()
    assert len(Meeting.objects.all()) == 1

    t = Topic(
        title="Test Meeting",
        meeting=m,
        experience_level="novice",
        length_minutes=10,
        description="Test Topic",
    )
    t.save()
    assert len(Topic.objects.all()) == 1

    r = ["test@email.com"]

    email.send_meeting_topic_submitted_email(t, r)
    assert len(mail.outbox) == 1


def test_anonymous_rsvp_email():
    m = Meeting(
        when=datetime.datetime.now(), reg_close_date=datetime.datetime.now(), description="Test",
    )
    m.save()
    assert len(Meeting.objects.all()) == 1

    rsvp = RSVP(
        last_name="last name",
        first_name="first_name",
        email="test@test.com",
        meeting=m,
        response="Y",
    )
    rsvp.save()
    assert len(RSVP.objects.all()) == 1

    email.send_rsvp_email(rsvp)
    assert len(mail.outbox) == 1


class MeetingTitleTest(TestCase):
    # Tests if 'custom_title' from 'meeting' is available, it'll be used as
    # 'title' for meeting.  If 'custom_title' from 'meeting' isn't available,
    # the 'default_title' from 'meeting_type' will be used as 'title' for
    # meeting.

    def setUp(self):
        self.meeting_type_non_main = MeetingType.objects.create(
            name="Non Main Sig ", default_title="Non Main Default Title"
        )

    def test_non_main_meeting_without_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), meeting_type=self.meeting_type_non_main
        )
        self.assertEqual(meeting.title, "Non Main Default Title")

    def test_main_meeting_without_custom_field(self):
        meeting = Meeting.objects.create(when=datetime.date.today())
        self.assertEqual(meeting.title, "In the Loop")

    def test_non_main_meeting_with_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(),
            meeting_type=self.meeting_type_non_main,
            custom_title="Non Main Custom Title",
        )
        self.assertEqual(meeting.title, "Non Main Custom Title")

    def test_main_meeting_with_custom_field(self):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), custom_title="Main Custom Title"
        )
        self.assertEqual(meeting.title, "Main Custom Title")


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_rsvp_works_for_anonymous_user(client):
    meeting = Meeting.objects.create(when=datetime.date.today() + datetime.timedelta(days=1))
    route = reverse("rsvp")
    response = client.post(
        route,
        data={
            "meeting": meeting.id,
            "first_name": "Some",
            "last_name": "Body",
            "email": "somebody@example.com",
        },
    )
    assert response.status_code == 200


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_rsvp_fails_gracefully_with_missing_data(client):
    meeting = Meeting.objects.create(when=datetime.date.today() + datetime.timedelta(days=1))
    response = client.post(reverse("rsvp"), data={"meeting": meeting.id})
    assert response.status_code == 200


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_topics_drafts_list_view(client, django_user_model):
    username = "testtesterson"
    password = "bar"

    user1 = django_user_model.objects.create_user(username=username, password=password)

    pr1 = Presentor(user=user1, name="u1")
    pr1.save()

    topic1 = Topic(title="test1")
    topic1.save()
    topic1.presentors.add(pr1)
    topic2 = Topic(title="not-selected")
    topic2.save()

    client.login(username=username, password=password)
    response = client.get(reverse('propose_topics_user'))
    assert list(response.context['topics'].values_list('id', flat=True)) == [user1.id]


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_topics_drafts_add_view(client, django_user_model):
    username = "testtesterson"
    password = "bar"

    user1 = django_user_model.objects.create_user(username=username, password=password)

    pr1 = Presentor(user=user1, name="u1")
    pr1.save()

    topic1 = Topic(title="test1")
    topic1.save()
    topic1.presentors.add(pr1)

    client.login(username=username, password=password)

    data = {"title": "some title", "description": "some desc"}
    response = client.post(reverse('propose_topic_user', args=(topic1.id,)), data)

    assert response.status_code == 302
    assert topic1.drafts.count() == 1
