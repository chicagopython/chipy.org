import datetime

import pytest
from django.core import mail

from chipy_org.apps.meetings.models import Meeting, Topic

from .. import email

pytestmark = pytest.mark.django_db


def test_post_topic_sends_email():
    meeting = Meeting(
        when=datetime.datetime.now(),
        reg_close_date=datetime.datetime.now(),
        description2="Test",
        in_person_capacity=5,
    )
    meeting.save()
    assert len(Meeting.objects.all()) == 1

    topic = Topic(
        title="Test Meeting",
        meeting=meeting,
        experience_level="novice",
        length=10,
        description2="Test Topic",
    )
    topic.save()
    assert len(Topic.objects.all()) == 1

    email.send_meeting_topic_submitted_email(topic, ["test@email.com"])
    assert len(mail.outbox) == 1
