# pylint: disable=redefined-outer-name

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from chipy_org.apps.meetings.models import Meeting, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture
def meeting():
    return Meeting.objects.create(when="1994-01-01", in_person_capacity=10)


@pytest.fixture
def user():
    return User.objects.get_or_create(username="test_user")[0]


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def staff_client(authenticated_client, user):
    user.is_staff = True
    user.save()
    return authenticated_client


class TestPastTopics:
    @staticmethod
    def test_cannot_see_past_topics_only_approved(client):
        topic = Topic.objects.create(
            title="Some python talk",
            status=Topic.StatusChoice.CONFIRMED,
        )
        response = client.get(reverse("past_topics"))
        assert response.status_code == 200
        assert not topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_cannot_see_past_topics_only_assigned_to_meeting(client, meeting):
        topic = Topic.objects.create(
            title="Some python talk",
            meeting=meeting,
        )
        response = client.get(reverse("past_topics"))
        assert response.status_code == 200
        assert not topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_can_see_past_topics_approved_and_assigned_to_a_meeting(client, meeting):
        topic = Topic.objects.create(
            title="Some python talk", status=Topic.StatusChoice.CONFIRMED, meeting=meeting
        )
        response = client.get(reverse("past_topics"))
        assert response.status_code == 200
        assert topic.title.encode("utf-8").lower() in response.content.lower()


class TestPendingTopics:
    @staticmethod
    def test_does_not_work_for_unauthed_user(client):
        response = client.get(reverse("pending_topics"))
        assert response.status_code == 302

    @staticmethod
    def test_does_not_work_for_non_staff_authed_use(authenticated_client):
        response = authenticated_client.get(reverse("pending_topics"))
        assert response.status_code == 302

    @staticmethod
    def test_works_for_staff(authenticated_client, user):
        user.is_staff = True
        user.save()
        response = authenticated_client.get(reverse("pending_topics"))
        assert response.status_code == 200

    @staticmethod
    def test_can_see_past_topics_only_approved(staff_client):
        topic = Topic.objects.create(
            title="Some python talk",
            status=Topic.StatusChoice.CONFIRMED,
        )
        response = staff_client.get(reverse("pending_topics"))
        assert response.status_code == 200
        assert topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_can_see_past_topics_only_assigned_to_meeting(staff_client, meeting):
        topic = Topic.objects.create(
            title="Some python talk",
            meeting=meeting,
        )
        response = staff_client.get(reverse("pending_topics"))
        assert response.status_code == 200
        assert topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_cannot_see_past_topics_approved_and_assigned_to_a_meeting(staff_client, meeting):
        topic = Topic.objects.create(
            title="Some python talk", status=Topic.StatusChoice.CONFIRMED, meeting=meeting
        )
        response = staff_client.get(reverse("pending_topics"))
        assert response.status_code == 200
        assert not topic.title.encode("utf-8").lower() in response.content.lower()
