# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_auto_20190711_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='name',
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
    ]
