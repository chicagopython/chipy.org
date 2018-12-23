# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_meeting_reg_close_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rsvp',
            name='response',
            field=models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')]),
        ),
    ]
