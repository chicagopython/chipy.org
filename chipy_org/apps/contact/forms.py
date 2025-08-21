import logging

from django import forms
from django.conf import settings
from django_recaptcha.fields import ReCaptchaField

from chipy_org.libs.custom_captcha import CrispyReCaptchaV2Checkbox
from chipy_org.libs.email import send_email

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].label = False

    sender = forms.CharField(max_length=256, label="From")
    email = forms.EmailField(max_length=256)
    subject = forms.CharField(max_length=256)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs=dict(cols=19, rows=10, placeholder="2000 character limit")),
    )
    captcha = ReCaptchaField(widget=CrispyReCaptchaV2Checkbox, label="")

    def send_email(self):
        # NOTE: from_email MUST be the verified SendGrid email address
        # which should always be set in settings.DEFAULT_FROM_EMAIL
        # SendGrid will NOT send an email from a random unverified email address.
        # send_email has this value set as a default, and it should not be overwritten.
        # reply_to is set as the requester's email so that when an  organizer replies
        # the reply goes to the email entered by the user in the contact form.
        send_email(
            recipients=getattr(settings, "ENVELOPE_EMAIL_RECIPIENTS", []),
            subject=self.cleaned_data["subject"],
            body=self.cleaned_data["message"],
            reply_to=[self.cleaned_data["email"]],
        )
