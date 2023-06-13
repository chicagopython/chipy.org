import logging

from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

logger = logging.getLogger(__name__)


def send_meeting_topic_submitted_email(topic, recipients):  # pylint: disable=invalid-name
    try:
        plaintext = get_template("talks/emails/meeting_topic_submitted.txt")
        htmly = get_template("talks/emails/meeting_topic_submitted.html")
        context = {"topic": topic, "site": Site.objects.get_current()}
        subject = "Chipy: New Meeting Topic Submitted"
        from_email = "DoNotReply@chipy.org"
        text_content = plaintext.render(context)
        html_content = htmly.render(context)
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.exception(e)
