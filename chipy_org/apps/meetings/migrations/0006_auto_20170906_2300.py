# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0005_auto_20170906_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='meeting',
            field=models.ForeignKey(related_name='topics', blank=True, to='meetings.Meeting', help_text="Please select the meeting that you'd like to target your talk for.", null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='notes',
            field=models.TextField(help_text='Additional non-public information or context you want us to know about the talk submission.', null=True, verbose_name='Private Submission Notes', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='title',
            field=models.CharField(help_text='This will be the public title for your talk.', max_length=255),
        ),
    ]
