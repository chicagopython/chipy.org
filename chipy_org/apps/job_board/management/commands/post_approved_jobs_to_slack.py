import json
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader

from chipy_org.apps.job_board.models import JobPost

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command retrieves all approved and active job posts from the database
    and posts them to the slack jobs channel. 
    
    Integrate this command with a scheduler to automatically post jobs to the 
    slack jobs channel.  
    """

    def handle(self, *args, **options):
        print("These are the Active Postings on the Job Board", "\n")
        posts = JobPost.approved_and_active.all()

        if posts.count():
            context = {"posts": posts}
            template = loader.get_template("job_board/slack_template.txt")
            msg = template.render(context)

            job_post_key = settings.JOB_POST_KEY
            webhook_url = f"https://hooks.slack.com/services/{job_post_key}"
            slack_data = {"text": msg}

            response = requests.post(
                webhook_url,
                data=json.dumps(slack_data),
                headers={"Content-Type": "application/json"},
            )

            if response.status_code != 200:
                logger.info("Failed to post to slack job channel.")
