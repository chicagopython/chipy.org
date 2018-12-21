# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def change_maybe_to_yes(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    RSVP = apps.get_model("meetings", "RSVP")
    for rsvp in RSVP.objects.filter(response="M"):
        rsvp.response = "Y"
        rsvp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_meeting_reg_close_date'),
    ]

    operations = [migrations.RunPython(change_maybe_to_yes)]
