# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


has_probablepeople = True
try:
    import probablepeople
except:
    has_probablepeople = False


def parse_anonymous_rsvp_names(apps, schema_editor):
    if not has_probablepeople:
        return None

    RSVP = apps.get_model('meetings', 'RSVP')
    anonymous_rsvps = RSVP.objects.filter(user=None)
    for rsvp in anonymous_rsvps:
        if rsvp.name:
            parsed = probablepeople.tag(rsvp.name)
            rsvp.first_name = parsed[0].get('GivenName','').lower()
            rsvp.last_name = parsed[0].get('Surname').lower()
            rsvp.save()


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0011_merge'),
    ]

    operations = [
        migrations.RunPython(parse_anonymous_rsvp_names),
    ]
