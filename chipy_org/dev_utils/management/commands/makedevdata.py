import random
import string
import sys
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from chipy_org.apps import announcements, job_board, meetings, sponsors


class Command(BaseCommand):
    help = "Adds initial data to the site for development and testing purposes."

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
        site, _ = Site.objects.get_or_create(domain="example.com")
        for title in ["conduct", "donate", "giving", "host", "referrals", "sigs", "volunteer"]:
            page, _ = FlatPage.objects.get_or_create(
                url=f"/{title}/",
                title=title,
                content="Here is a page with content",
            )
            page.sites.add(site)

        # Add a user
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

        # Announcements
        for announcement in announcements.models.Announcement.objects.filter(
            headline__startswith="Dev"
        ):
            announcement.delete()

        for k, v in times.items():
            announcements.models.Announcement.objects.update_or_create(
                headline=f"Dev Headline - {k}",
                text="Dev Announcement",
                active=True,
                end_date=v,
            )

        # Meetings
        presenter, _ = meetings.models.Presenter.objects.get_or_create(
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

        for meeting in meetings.models.Meeting.objects.filter(key__startswith="dev"):
            meeting.delete()

        count = 0
        for k, v in times.items():
            meeting, _ = meetings.models.Meeting.objects.update_or_create(
                where=venue,
                when=v + timedelta(days=7),
                description=f"Dev Meeting {k}".title(),
                reg_close_date=(v + timedelta(days=6)),
                key=f"dev{count:037}",
                in_person_capacity=5,
            )

            topic, _ = meetings.models.Topic.objects.get_or_create(
                meeting=meeting,
                experience_level="novice",
                length=10,
                title=f"Saponification - Part {count}",
                description=f"Saponification - Part {count}",
                status=meetings.models.Topic.StatusChoice.CONFIRMED,
            )
            topic.presenters.set((presenter,))

            count += 1

        # Add a bunch of past meetings too for pagination testing
        for _ in range(10):
            meeting_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=40))
            random_days_ago = random.randint(10, 30)
            meeting_date = now - timedelta(days=random_days_ago)
            meeting_description = f"Dev meeting{random.randint(1000, 2000)}"
            meeting_registration_end = meeting_date + timedelta(days=6)

            meeting, _ = meetings.models.Meeting.objects.update_or_create(
                where=venue,
                when=meeting_date,
                description=meeting_description,
                reg_close_date=meeting_registration_end,
                key=meeting_id,
                in_person_capacity=5,
            )

        # Jobs
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

        # Sponsors
        sponsor_levels = [("Platinum", 1), ("Gold", 2), ("Silver", 3), ("Bronze", 4)]
        sponsor_groups = dict()

        for name, list_priority in sponsor_levels:
            sponsor_group, _ = sponsors.models.SponsorGroup.objects.update_or_create(
                name=name,
                list_priority=list_priority,
            )
            sponsor_groups[name] = sponsor_group

        some_sponsors = [
            ("Car company", "car-company", "A major one", "Platinum"),
            ("Lou's Place", "lous-place", "A random bar", "Gold"),
            ("Planet Starbucks", "planet-starbucks", "For your latte's in space.", "Silver"),
            ("IBM Stellar Sphere", "ibm", "Making old tech new", "Bronze"),
            ("The Microsoft Galaxy", "msft", "Newly discovered", "Bronze"),
        ]

        for name, slug, description, sponsor_level in some_sponsors:
            sponsors.models.Sponsor.objects.update_or_create(
                name=name,
                slug=slug,
                description=description,
                sponsor_group=sponsor_groups[sponsor_level],
            )
