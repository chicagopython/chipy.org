from django.db import migrations
from chipy_org.apps.meetings.models import Topic
import logging
logger = logging.getLogger(__file__)


def forwards(apps, schema_editor):
    for topic in Topic.objects.all():
        try:
            topic.description2 = topic.description
            topic.save()
        except AttributeError:
            logger.info("Couldn't migrate data for object: %s", topic)
            continue


class Migration(migrations.Migration):

    dependencies = [
        ("meetings", "0009_topic_description2"),
    ]

    operations = [
        # migrations.RunPython(forwards),
    ]
