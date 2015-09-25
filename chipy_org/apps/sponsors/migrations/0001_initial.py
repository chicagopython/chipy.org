# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(null=True, verbose_name='About this sponsorship', blank=True)),
                ('about_short', models.CharField(max_length=128, null=True, verbose_name='Brief description of sponsorship', blank=True)),
            ],
            options={
                'ordering': ['sponsor__name'],
                'verbose_name': 'General Sponsor',
                'verbose_name_plural': 'General Sponsors',
            },
        ),
        migrations.CreateModel(
            name='MeetingSponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about', models.TextField(null=True, verbose_name='About this sponsorship', blank=True)),
                ('about_short', models.CharField(max_length=128, null=True, verbose_name='Brief description of sponsorship', blank=True)),
                ('meeting', models.ForeignKey(related_name='meeting_sponsors', to='meetings.Meeting')),
            ],
            options={
                'ordering': ['sponsor__name'],
                'verbose_name': 'Meeting Sponsor',
                'verbose_name_plural': 'Meeting Sponsors',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('slug', models.SlugField(max_length=80)),
                ('url', models.URLField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', models.ImageField(help_text='All logos will be cropped to fit a 4 by 3 aspect ratio. Resolution should be at minimum 400x300.', null=True, upload_to='sponsor_logos', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='meetingsponsor',
            name='sponsor',
            field=models.ForeignKey(to='sponsors.Sponsor'),
        ),
        migrations.AddField(
            model_name='generalsponsor',
            name='sponsor',
            field=models.ForeignKey(to='sponsors.Sponsor'),
        ),
    ]
