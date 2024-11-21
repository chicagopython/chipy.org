from django.db import migrations
from chipy_org.apps.announcements.models import Announcement
import logging
logger = logging.getLogger(__file__)

def forwards(apps, schema_editor):
    for announcement in Announcement.objects.all():
        try:
            announcement.text2 = announcement.text
            announcement.save()
        except AttributeError:
            logger.info("Couldn't migrate data for object: %s", announcement)
            continue

class Migration(migrations.Migration):

    dependencies = [
        ("announcements", "0003_announcement_text2"),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
