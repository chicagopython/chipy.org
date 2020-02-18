# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_squashed_0015_auto_20200208_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='custom_title',
            field=models.CharField(max_length=64, blank=True, null=True, help_text="If you fill out this field, this 'custom_title'will show up as the title of the event."),
        ),
    ]
