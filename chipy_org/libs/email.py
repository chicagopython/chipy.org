import logging

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives

logger = logging.getLogger(__name__)


def enforce_list(value):
    if isinstance(value, str):
        return [value]
    return value


def send_email(recipients, subject, body, html_body=None, reply_to=None, swallow_errors=False):
    """Helper to standardize sending of email"""
    recipients = enforce_list(recipients)
    reply_to = enforce_list(reply_to or [])

    params = {
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "to": recipients,
        "subject": subject,
        "body": body,
        "reply_to": enforce_list(reply_to or settings.DEFAULT_FROM_EMAIL),
    }
    if html_body:
        message = EmailMultiAlternatives(**params)
        message.attach_alternative(html_body, "text/html")
    else:
        message = EmailMessage(**params)

    try:
        message.send()
    except Exception:
        logger.exception("Error sending email with subject %s", subject)
        if not swallow_errors:
            raise
