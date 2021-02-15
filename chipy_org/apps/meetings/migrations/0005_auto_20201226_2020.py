# Generated by Django 2.2.17 on 2020-12-26 20:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0004_add_cc0_license'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Presentor',
            new_name='Presenter',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='presentors',
            new_name='presenters',
        ),
    ]
