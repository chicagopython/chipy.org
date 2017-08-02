# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('headline', models.TextField(max_length='100')),
                ('text', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('active', models.BooleanField(default=True, help_text='Has this announcement been published yet?')),
                ('photo', models.ImageField(null=True, upload_to='announcements', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
