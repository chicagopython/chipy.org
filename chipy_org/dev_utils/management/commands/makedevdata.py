import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from chipy_org.apps import announcements, job_board, meetings, profiles, sponsors, subgroups

from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Adds initial development data to the site; useful when developing locally'

    def handle(self, *args, **options):
        print("hello from make dev")

        # check that this is a development enviornment if not exit
        if not settings.DEBUG:
            print("""
            DEBUG is not set to True.
            Exiting without making and changes to database.
            """)
            sys.exit(0)

        # make some users
        tyler, _ = User.objects.get_or_create(
            username = "tdurden",
            first_name="tyler",
            last_name="durden",
        )

        # announcement data
        announce, _ = announcements.models.Announcement.objects.get_or_create(
            headline="Test Headline",
            text="Text Announcement",
            active=True,
        )
        announce.end_date=(datetime.now() + timedelta(days=30))
        announce.save()

        # meetings data
        venue, _ = meetings.models.Venue.objects.get_or_create(
            name="Paper Street House",
            email="tyler.durden@paperstreetsoap.com",
            phone="288-555-0153",
            address="1537 Paper Street, Bradford DE 19808",
        )
        
        now = datetime.now()

        for m in meetings.models.Meeting.objects.filter(key="test"):
            m.delete()

        meeting, _ = meetings.models.Meeting.objects.update_or_create(
            where=venue,
            when=now+timedelta(days=7),
            description="test data for __main__  meeting",
            reg_close_date=(now +  timedelta(days=6)),
            key="forty"
        )

        # presentor, _ = meetings.models.Presentor.objects.get_or_create(
        #     user=tyler,
        #     name= tyler.first_name + " " + tyler.last_name,
        #     email=tyler.email,
        #     release=True
        # )

        # topic, _ = meetings.models.Topic.objects.get_or_create(
        #     presentors=tyler,
        #     meeting=None,
        #     experience_level="novice",
        #     length=10,
        #     description="saponification",
        # )
        
        # jobs data
        job_post = job_board.models.JobPost(
            company_name="Paper Street Soap",
            position="Web Developer",
            description="",
            is_sponsor=False,
            can_host_meeting=True,
            time_to_expire=timedelta(days=60),
            location="CH",
            job_type="FT",
            contact= tyler,
            is_from_recruiting_agency=False,
            agree_to_terms=True,
        )
        job_post.save()

        # make some sponsors
        gold_sponsor = sponsors.models.SponsorGroup()
        gold_sponsor.save()
        sponsor = sponsors.models.Sponsor()
        sponsor.save()

        # make some subgroups
        # TBD