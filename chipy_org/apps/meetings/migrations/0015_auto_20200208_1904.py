# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0014_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='custom_title',
            field=models.CharField(max_length=64, blank=True, null=True, help_text="If you fill out this field, this 'custom_title' will show up as the title of the event."),
        ),
        migrations.AddField(
            model_name='meetingtype',
            name='default_title',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(blank=True, null=True, help_text='Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting. ', to='meetings.MeetingType'),
        ),
    ]
