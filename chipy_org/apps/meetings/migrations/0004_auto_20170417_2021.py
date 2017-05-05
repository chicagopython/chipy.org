# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subgroups', '0001_initial'),
        ('meetings', '0003_topic_experience_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
                ('subgroup', models.ForeignKey(blank=True, to='subgroups.SubGroup', help_text='Optional Sub-group (i.e. SIG)', null=True)),
            ],
            options={
                'verbose_name': 'Meeting Type',
                'verbose_name_plural': 'Meeting Types',
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(blank=True, to='meetings.MeetingType', help_text='Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting.', null=True),
        ),
    ]
