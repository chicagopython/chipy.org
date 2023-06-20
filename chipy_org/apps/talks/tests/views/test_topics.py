import pytest
from django.urls import reverse

from chipy_org.apps.meetings.models import Meeting, Topic

pytestmark = pytest.mark.django_db


@pytest.fixture
def meeting():
    return Meeting.objects.create(when="1994-01-01", in_person_capacity=10)


class TestPastTopics:
    @staticmethod
    def test_cannot_see_past_topics_only_approved(client):
        topic = Topic.objects.create(
            title="Some python talk",
            approved=True,
        )
        response = client.get(reverse("past_topics"), follow=True)
        assert response.status_code == 200
        assert not topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_cannot_see_past_topics_only_assigned_to_meeting(client, meeting):
        topic = Topic.objects.create(
            title="Some python talk",
            meeting=meeting,
        )
        response = client.get(reverse("past_topics"), follow=True)
        assert response.status_code == 200
        assert not topic.title.encode("utf-8").lower() in response.content.lower()

    @staticmethod
    def test_can_see_past_topics_approved_and_assigned_to_a_meeting(client, meeting):
        topic = Topic.objects.create(title="Some python talk", approved=True, meeting=meeting)
        response = client.get(reverse("past_topics"), follow=True)
        assert response.status_code == 200
        assert topic.title.encode("utf-8").lower() in response.content.lower()
