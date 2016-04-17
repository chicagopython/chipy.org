import logging
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.conf import settings


logger = logging.getLogger(__name__)

def send_rsvp_email(rsvp):
    try:
        plaintext = get_template('meetings/emails/rsvp_email.txt')
        htmly = get_template('meetings/emails/rsvp_email.html')

        d = Context(
            {'key': rsvp.key, 'site': Site.objects.get_current()})

        subject = 'Chipy: Link to Change your RSVP'
        from_email = 'DoNotReply@chipy.org'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, [rsvp.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.exception(e)


def send_meeting_topic_submitted_email(topic):
    try:
        plaintext = get_template('meetings/emails/meeting_topic_submitted.txt')
        htmly = get_template('meetings/emails/meeting_topic_submitted.html')
        chipy_topic_emails = getattr(settings, "CHIPY_TOPIC_SUBMIT_EMAILS")
        recipients = getattr(settings, "CHIPY_TOPIC_SUBMIT_EMAILS", [])
        d = Context(
            {'topic': topic, 'site': Site.objects.get_current()})

        subject = 'Chipy: New Meeting Topic Submitted'
        from_email = 'DoNotReply@chipy.org'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(
            subject, text_content, from_email,
            recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        logger.exception(e)
