# pylint: disable=invalid-name,no-member,unused-variable,duplicate-code,redefined-outer-name
import datetime
import random
import string

import pytest

from chipy_org.apps.meetings.models import Meeting, Topic, Venue

pytestmark = pytest.mark.django_db


@pytest.fixture
def random_meeting_key():
    "returns a alpha numeric string of 40 characterst to comply with the meeting key"
    return "".join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))


@pytest.fixture
def venue():
    v = Venue.objects.create(name="Test")
    return v


@pytest.fixture
def meeting_in_past(random_meeting_key):
    m = Meeting.objects.create(
        when=datetime.date.today() - datetime.timedelta(days=30),
        key=random_meeting_key,
        in_person_capacity=5,
    )
    return m


@pytest.fixture
def meeting_in_future_registration_closed(random_meeting_key):
    m = Meeting.objects.create(
        when=datetime.date.today() + datetime.timedelta(days=30),
        key=random_meeting_key,
        reg_close_date=datetime.date.today() - datetime.timedelta(days=1),
        in_person_capacity=5,
    )
    return m


class TestMeetings:
    @staticmethod
    def test_api_returns_401_unauthenticated(client, venue):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=venue, in_person_capacity=5
        )
        response = client.get("/api/meetings/")

        assert response.status_code == 403

    @staticmethod
    def test_api_returns_meetings(client, venue):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=venue, in_person_capacity=5
        )
        response = client.get("/api/meetings/", headers={"Api-Key": "usethisintest"})

        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1

        record = data[0]
        assert record["id"] == meeting.id
        assert record["when"] == meeting.when.strftime("%Y-%m-%dT%H:%M:%S")
        assert record["live_stream"] is None
        assert record["topics"] == []

        location = record["where"]
        assert location["id"] == 1
        assert location["created"] == venue.created.strftime("%Y-%m-%dT%H:%M:%S.%f")
        assert location["modified"] == venue.modified.strftime("%Y-%m-%dT%H:%M:%S.%f")
        assert location["name"] == venue.name
        assert location["email"] is None  # TODO: We should not share this # pylint: disable=W0511
        assert location["phone"] is None  # TODO: We should not share this # pylint: disable=W0511
        assert location["address"] is None
        assert location["directions"] is None
        assert location["embed_map"] is None
        assert location["link"] is None

    @staticmethod
    def test_api_returns_backup_reviewers(client, venue):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=venue, in_person_capacity=5
        )
        topic = Topic.objects.create(title="test topic", meeting=meeting)
        response = client.get("/api/meetings/", headers={"Api-Key": "usethisintest"})

        assert response.status_code == 200
        record = response.json()[0]
        topic = record["topics"][0]
        assert topic["reviewers"] == [
            "pete@example.com",
            "carl@example.com",
        ]

    @staticmethod
    def test_api_returns_extra_review_if_specified(client, venue):
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=venue, in_person_capacity=5
        )
        topic = Topic.objects.create(
            title="test topic", meeting=meeting, requested_reviewer="heather@example.com"
        )
        response = client.get("/api/meetings/", headers={"Api-Key": "usethisintest"})

        assert response.status_code == 200
        record = response.json()[0]
        assert record["id"] == meeting.id
        topic_record = record["topics"][0]
        assert topic_record["reviewers"] == [
            topic.requested_reviewer,
            "pete@example.com",
            "carl@example.com",
        ]
