# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20170417_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='notes',
            field=models.TextField(help_text='(optional) additional non-public information or context you want us to know about the talk submission.', null=True, verbose_name='Private Submission Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='description',
            field=models.TextField(help_text='This will be the public talk description.', null=True, verbose_name='Public Description', blank=True),
        ),
    ]
