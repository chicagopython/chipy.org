# Generated by Django 5.1.3 on 2024-11-20 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meetings", "0012_meetings_move_ckeditor_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="meeting",
            name="description",
        ),
        migrations.RemoveField(
            model_name="meetingtype",
            name="description",
        ),
        migrations.RemoveField(
            model_name="topic",
            name="description",
        ),
    ]
