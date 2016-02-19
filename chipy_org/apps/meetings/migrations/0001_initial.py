# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import interval.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('when', models.DateTimeField()),
                ('key', models.CharField(unique=True, max_length=40, blank=True)),
                ('live_stream', models.CharField(max_length=500, null=True, blank=True)),
                ('meetup_id', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Presentor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('release', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RSVP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('response', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No'), ('M', 'Maybe')])),
                ('key', models.CharField(max_length=255, null=True, blank=True)),
                ('meetup_user_id', models.IntegerField(null=True, blank=True)),
                ('meeting', models.ForeignKey(to='meetings.Meeting')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('license', models.CharField(default='CC BY', max_length=50, choices=[('CC BY', 'Creative Commons: Attribution'), ('CC BY-SA', 'Creative Commons: Attribution-ShareAlike'), ('CC BY-ND', 'Creative Commons: Attribution-NoDerivs'), ('CC BY-NC', 'Creative Commons: Attribution-NonCommercial'), ('CC BY-NC-SA', 'Creative Commons: Attribution-NonCommercial-ShareAlike'), ('CC BY-NC-ND', 'Creative Commons: Attribution-NonCommercial-NoDerivs'), ('All Rights Reserved', 'All Rights Reserved')])),
                ('length', interval.fields.IntervalField(null=True, blank=True)),
                ('embed_video', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('slides_link', models.URLField(null=True, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('approved', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(related_name='topics', blank=True, to='meetings.Meeting', null=True)),
                ('presentors', models.ManyToManyField(to='meetings.Presentor', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('directions', models.TextField(null=True, blank=True)),
                ('embed_map', models.TextField(null=True, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meeting',
            name='where',
            field=models.ForeignKey(blank=True, to='meetings.Venue', null=True),
        ),
    ]
