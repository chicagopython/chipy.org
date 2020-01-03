# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0010_auto_20191231_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='length',
        ),
    ]
