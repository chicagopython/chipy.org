# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20160222_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='python_level',
        ),
        migrations.AddField(
            model_name='topic',
            name='experience_level',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Audience Experience Level', choices=[('novice', 'Novice'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]),
        ),
    ]
