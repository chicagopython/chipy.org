import sys
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from chipy_org.apps import announcements, job_board, meetings, profiles, sponsors, subgroups


class Command(BaseCommand):
    help = "Adds initial data to the site for developement and testing purposes."

    def handle(self, *args, **options):

        if not settings.DEBUG:
            print(
                """
            DEBUG is not set to True.
            Exiting without making and changes to database.
            """
            )
            sys.exit(0)

        now = datetime.now()
        future = now + timedelta(days=30)
        past = now - timedelta(days=30)
        times = {"past": past, "now": now, "future": future}

        # add user
        tyler, _ = User.objects.get_or_create(
            username="tdurden",
            first_name="tyler",
            last_name="durden",
            email="tdurden@paperstreet.com",
        )

        narrator, _ = User.objects.get_or_create(
            username="cornilias",
            first_name="cornilias",
            last_name="",
            email="narrator@paperstreet.com",
        )

        # announcement data'
        for a in announcements.models.Announcement.objects.filter(headline__startswith="Dev"):
            a.delete()

        for k, v in times.items():
            announcements.models.Announcement.objects.update_or_create(
                headline=f"Dev Headline - {k}", text="Dev Announcement", active=True, end_date=v,
            )

        # meetings data
        presentor, _ = meetings.models.Presentor.objects.get_or_create(
            user=tyler,
            name=tyler.first_name + " " + tyler.last_name,
            email=tyler.email,
            release=True,
        )

        venue, _ = meetings.models.Venue.objects.get_or_create(
            name="Paper Street House",
            email="tyler.durden@paperstreetsoap.com",
            phone="288-555-0153",
            address="1537 Paper Street, Bradford DE 19808",
        )

        for meeting in meetings.models.Meeting.objects.filter(key__startswith="Dev"):
            meeting.delete()

        count = 0
        for k, v in times.items():
            meeting, _ = meetings.models.Meeting.objects.update_or_create(
                where=venue,
                when=v + timedelta(days=7),
                description=f"Dev Meeting {k}".title(),
                reg_close_date=(v + timedelta(days=6)),
                key=f"Dev-{count:04}",
            )
            count += 1

            topic, _ = meetings.models.Topic.objects.get_or_create(
                meeting=meeting,
                experience_level="novice",
                length=10,
                title=f"Saponification - Part {count}",
                description=f"Saponification - Part {count}",
                approved=True,
            )
            topic.presentors.set((presentor,))

        for job in job_board.models.JobPost.objects.filter(position__startswith="DEV DATA"):
            job.delete()

        job_post = job_board.models.JobPost(
            company_name="Paper Street Soap Co.",
            position="DEV DATA - Web Developer",
            description="Web Developer",
            is_sponsor=False,
            can_host_meeting=True,
            time_to_expire=timedelta(days=60),
            location="CH",
            job_type="FT",
            contact=tyler,
            is_from_recruiting_agency=False,
            agree_to_terms=True,
        )
        job_post.approve()

        job_post = job_board.models.JobPost(
            company_name="A Major Car Company",
            position="DEV DATA - Keep things to yourself",
            description="You can do this job from home.",
            is_sponsor=True,
            can_host_meeting=True,
            time_to_expire=timedelta(days=60),
            location="CH",
            job_type="FT",
            contact=narrator,
            is_from_recruiting_agency=False,
            agree_to_terms=True,
        )
        job_post.approve()

        # make some sponsors
        gold_sponsor = sponsors.models.SponsorGroup.update_or_create(name="Gold", list_priority=1,)
        gold_sponsor.save()
