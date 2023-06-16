import logging

from django.contrib.sites.models import Site
from django.template.loader import get_template

from chipy_org.libs.email import send_email

logger = logging.getLogger(__name__)


def send_meeting_topic_submitted_email(topic, recipients):  # pylint: disable=invalid-name
    plaintext = get_template("talks/emails/meeting_topic_submitted.txt")
    htmly = get_template("talks/emails/meeting_topic_submitted.html")
    context = {"topic": topic, "site": Site.objects.get_current()}
    subject = "Chipy: New Meeting Topic Submitted"
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    send_email(recipients, subject, text_content, html_content, swallow_errors=True)
