# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0012_rsvp_migration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rsvp',
            options={'ordering': ['-meeting', 'last_name', 'first_name']},
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='response',
            field=models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No')]),
        ),
    ]
