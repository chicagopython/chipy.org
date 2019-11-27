# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0008_auto_20190711_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='description',
            field=tinymce.models.HTMLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=tinymce.models.HTMLField(help_text='This will be the public talk description.', null=True, verbose_name='Public Description', blank=True),
        ),
    ]
