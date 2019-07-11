# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_meeting_reg_close_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingtype',
            name='description',
            field=tinymce.models.HTMLField(null=True, blank=True),
        ),
    ]
