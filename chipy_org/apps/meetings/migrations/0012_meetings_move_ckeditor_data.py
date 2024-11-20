from django.db import migrations
from chipy_org.apps.meetings.models import Meeting, MeetingType
import logging
logger = logging.getLogger(__file__)


def forward_meetings(apps, schema_editor):
    for meeting in Meeting.objects.all():
        try:
            meeting.description2 = meeting.description
            meeting.save()
        except AttributeError:
            logger.info("Couldn't migrate data for object: %s", meeting)
            continue


def forward_meeting_types(apps, schema_editor):
    for meeting_type in MeetingType.objects.all():
        try:
            meeting_type.description2 = meeting_type.description
            meeting_type.save()
        except AttributeError:
            logger.info("Couldn't migrate data for object: %s", meeting_type)
            continue


class Migration(migrations.Migration):

    dependencies = [
        ("meetings", "0011_meeting_descripiton2_meetingtype_description2_and_more"),
    ]

    operations = [
        migrations.RunPython(forward_meetings),
        migrations.RunPython(forward_meeting_types),
    ]
