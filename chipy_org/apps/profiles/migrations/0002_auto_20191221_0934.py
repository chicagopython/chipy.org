# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(verbose_name='Name for Security Check In', max_length=200),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='show',
            field=models.BooleanField(verbose_name='Show my information in the member list', default=False),
        ),
    ]
