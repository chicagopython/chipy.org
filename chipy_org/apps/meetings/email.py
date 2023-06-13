import logging

from django.contrib.sites.models import Site
from django.template.loader import get_template

from chipy_org.libs.email import send_email

logger = logging.getLogger(__name__)


def send_rsvp_email(rsvp):
    plaintext = get_template("meetings/emails/rsvp_email.txt")
    htmly = get_template("meetings/emails/rsvp_email.html")
    context = {"rsvp": rsvp, "site": Site.objects.get_current()}
    subject = "Chipy: Link to Change your RSVP"
    text_content = plaintext.render(context)
    html_content = htmly.render(context)
    send_email(rsvp.email, subject, text_content, html_content, swallow_errors=True)
