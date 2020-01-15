# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import probablepeople


def display_name_to_rsvps(apps, schema_editor):
    UserProfile = apps.get_model('profiles', 'UserProfile')
    RSVP = apps.get_model('meetings', 'RSVP')
    users = UserProfile.objects.all()
    for user in users:
        parsed = probablepeople.tag(user.display_name)
        first_name = parsed[0].get("GivenName")
        last_name = parsed[0].get("Surname")
        
        rsvps = RSVP.objects.filter(user=user.pk)
        for rsvp in rsvps:
            rsvp.first_name = first_name
            rsvp.last_name = last_name
            rsvp.save()
    

class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_merge'),
    ]

    operations = [
        migrations.RunPython(display_name_to_rsvps),
    ]
