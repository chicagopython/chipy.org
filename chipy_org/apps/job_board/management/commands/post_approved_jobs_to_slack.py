import datetime


import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader

from chipy_org.apps.job_board.models import JobPost
from chipy_org.libs.slack_utils import post_message_to_slack

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command retrieves all approved and active job posts from the database
    and posts them to the slack jobs channel. 
    
    Integrate this command with a scheduler to automatically post jobs to the 
    slack jobs channel.  
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "weekdays",
            nargs="+",
            type=int,
            help="""
            The desired weekdays to post represented an integer where Monday=0, Tuesday=1, ... , Saturday=5, and Sunday=6.
            Posts to the slack channel will only occur on the selected weekdays.
            """,
        )

    def handle(self, *args, **options):
        posts = JobPost.approved_and_active.all()

        if posts.count() and datetime.date.today().weekday() in options["weekdays"]:
            context = {"posts": posts}
            template = loader.get_template("job_board/slack_template.txt")
            msg = template.render(context)
            job_post_key = settings.JOB_POST_KEY

            try:
                post_message_to_slack(
                    channel_key=job_post_key, channel_name="job board", message=msg
                )
            except requests.HTTPError as error:
                logger.error(error)
                print(error)
