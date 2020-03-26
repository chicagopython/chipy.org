# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-26 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20200326_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repeatmeeting',
            name='registration_close_day_to_repeat',
            field=models.CharField(choices=[('Sun', 'Sun'), ('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'), ('Thur', 'Thur'), ('Fri', 'Fri'), ('Sat', 'Sat')], default='Mon', max_length=12),
        ),
    ]
