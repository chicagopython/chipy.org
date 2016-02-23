# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0002_rsvp_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='python_level',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[('novice', 'Novice'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]),
        ),
    ]
