# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-09 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sponsors', '0002_auto_20191021_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=10)),
                ('is_sponsor', models.BooleanField(default=False, verbose_name='Is the company a sponsor of ChiPy?')),
                ('can_host_meeting', models.BooleanField(default=False, verbose_name='Is your organization interested in hosting an event?')),
                ('approval_date', models.DateTimeField(blank=True, null=True)),
                ('link_to_company_page', models.CharField(max_length=255)),
                ('company_sponsor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sponsors.Sponsor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]