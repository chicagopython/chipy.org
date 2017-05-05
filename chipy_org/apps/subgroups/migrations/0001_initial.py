# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('image', models.ImageField(null=True, upload_to=b'group_images', blank=True)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(null=True, blank=True)),
                ('organizers', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'Sub Group (SIG)',
                'verbose_name_plural': 'Sub Groups (SIGs)',
            },
        ),
    ]
