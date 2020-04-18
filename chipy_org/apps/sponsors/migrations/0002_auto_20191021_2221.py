# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SponsorGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80)),
                ('list_priority', models.IntegerField(default=5)),
            ],
        ),
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_group',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                related_name='sponsors', blank=True, to='sponsors.SponsorGroup', null=True),
        ),
    ]
