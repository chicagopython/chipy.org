# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0003_topic_python_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='python_level',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Python Level', choices=[('novice', 'Novice'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')]),
        ),
    ]
