# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-14 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_board', '0010_auto_20200414_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobpost',
            name='days_to_expire',
            field=models.IntegerField(default=30, verbose_name='Num of days for post to show'),
        ),
    ]
