# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='end_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
