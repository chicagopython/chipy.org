import datetime

import pytest
from django.core import mail

from chipy_org.apps.meetings.models import Meeting, Topic

from .. import email

pytestmark = pytest.mark.django_db


def test_post_topic_sends_email():
    m = Meeting(
        when=datetime.datetime.now(),
        reg_close_date=datetime.datetime.now(),
        description="Test",
        in_person_capacity=5,
    )
    m.save()
    assert len(Meeting.objects.all()) == 1

    t = Topic(
        title="Test Meeting",
        meeting=m,
        experience_level="novice",
        length=10,
        description="Test Topic",
    )
    t.save()
    assert len(Topic.objects.all()) == 1

    r = ["test@email.com"]

    email.send_meeting_topic_submitted_email(t, r)
    assert len(mail.outbox) == 1
