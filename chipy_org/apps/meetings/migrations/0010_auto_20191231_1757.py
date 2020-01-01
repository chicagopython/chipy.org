# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_length_minutes(apps, schema_editor):
    Topic = apps.get_model('meetings', 'Topic')
    for topic in Topic.objects.all():
        try:
            minutes = int(topic.length.total_seconds()/60)
            topic.length_minutes = minutes
            topic.save()
        except:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0009_auto_20191231_1735'),
    ]

    operations = [
        migrations.RunPython(populate_length_minutes),
    ]
