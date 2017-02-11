# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('slug', models.SlugField(max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
                ('organizers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meetingtype',
            name='subgroup',
            field=models.ForeignKey(blank=True, to='meetings.SubGroup', help_text='Optional Sub-group (i.e. SIG)', null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(blank=True, to='meetings.MeetingType', help_text='Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting.', null=True),
        ),
    ]
