# Generated by Django 5.1.3 on 2024-11-20 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("announcements", "0004_move_ckeditor_data_to_field"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="announcement",
            name="text",
        ),
    ]
