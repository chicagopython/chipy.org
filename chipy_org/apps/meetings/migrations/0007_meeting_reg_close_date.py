# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_auto_20170906_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='reg_close_date',
            field=models.DateTimeField(null=True, verbose_name='Registration Close Date', blank=True),
        ),
    ]
