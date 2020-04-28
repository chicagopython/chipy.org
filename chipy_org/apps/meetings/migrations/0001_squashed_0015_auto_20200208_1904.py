# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import tinymce.models


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# chipy_org.apps.meetings.migrations.0012_rsvp_migration
# chipy_org.apps.meetings.migrations.0010_auto_20191231_1757

class Migration(migrations.Migration):

    dependencies = [
        ('subgroups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('when', models.DateTimeField()),
                ('key', models.CharField(max_length=40, unique=True, blank=True)),
                ('live_stream', models.CharField(max_length=500, blank=True, null=True)),
                ('meetup_id', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Presentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, blank=True, null=True)),
                ('phone', models.CharField(max_length=255, blank=True, null=True)),
                ('release', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, blank=True, null=True)),
                ('email', models.EmailField(max_length=255, blank=True, null=True)),
                ('response', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No'), ('M', 'Maybe')])),
                ('key', models.CharField(max_length=255, blank=True, null=True)),
                ('meetup_user_id', models.IntegerField(blank=True, null=True)),
                ('meeting', models.ForeignKey(on_delete=models.deletion.CASCADE, to='meetings.Meeting')),
                ('user', models.ForeignKey(
                    on_delete=models.deletion.CASCADE,
                    blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('guests', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, help_text='This will be the public title for your talk.')),
                ('license', models.CharField(max_length=50, default='CC BY', choices=[('CC BY', 'Creative Commons: Attribution'), ('CC BY-SA', 'Creative Commons: Attribution-ShareAlike'), ('CC BY-ND', 'Creative Commons: Attribution-NoDerivs'), ('CC BY-NC', 'Creative Commons: Attribution-NonCommercial'), ('CC BY-NC-SA', 'Creative Commons: Attribution-NonCommercial-ShareAlike'), ('CC BY-NC-ND', 'Creative Commons: Attribution-NonCommercial-NoDerivs'), ('All Rights Reserved', 'All Rights Reserved')])),
                ('embed_video', models.TextField(blank=True, null=True)),
                ('description', tinymce.models.HTMLField(verbose_name='Public Description', blank=True, null=True, help_text='This will be the public talk description.')),
                ('slides_link', models.URLField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(
                    on_delete=models.deletion.CASCADE,
                    blank=True, 
                    null=True,
                    help_text="Please select the meeting that you'd like to target your talk for.",
                    related_name='topics',
                    to='meetings.Meeting')
                ),
                ('presentors', models.ManyToManyField(blank=True, to='meetings.Presentor')),
                ('experience_level', models.CharField(verbose_name='Audience Experience Level', max_length=15, blank=True, null=True, choices=[('novice', 'Novice'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])),
                ('notes', models.TextField(verbose_name='Private Submission Notes', blank=True, null=True, help_text='Additional non-public information or context you want us to know about the talk submission.')),
                ('length_minutes', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, blank=True, null=True)),
                ('phone', models.CharField(max_length=255, blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('directions', models.TextField(blank=True, null=True)),
                ('embed_map', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='where',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, blank=True, null=True, to='meetings.Venue'),
        ),
        migrations.CreateModel(
            name='MeetingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(max_length=64, unique=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('subgroup', models.ForeignKey(on_delete=models.deletion.CASCADE, blank=True, null=True, help_text='Optional Sub-group (i.e. SIG)', to='subgroups.SubGroup')),
            ],
            options={
                'verbose_name': 'Meeting Type',
                'verbose_name_plural': 'Meeting Types',
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_type',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                blank=True, null=True, help_text='Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting.', to='meetings.MeetingType'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='reg_close_date',
            field=models.DateTimeField(verbose_name='Registration Close Date', blank=True, null=True),
        ),
        migrations.AlterModelOptions(
            name='rsvp',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.RemoveField(
            model_name='rsvp',
            name='guests',
        ),
        migrations.AddField(
            model_name='rsvp',
            name='first_name',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='rsvp',
            name='last_name',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='description',
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=tinymce.models.HTMLField(verbose_name='Public Description', blank=True, null=True, help_text='This will be the public talk description.'),
        ),
        migrations.AlterModelOptions(
            name='rsvp',
            options={'ordering': ['-meeting', 'last_name', 'first_name']},
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='response',
            field=models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')]),
        ),
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
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                blank=True, null=True, help_text='Type of meeting (i.e. SIG Meeting, Mentorship Meeting, Startup Row, etc.). Leave this empty for the main meeting. ', to='meetings.MeetingType'),
        ),
    ]
