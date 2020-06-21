import logging

from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from nocaptcha_recaptcha.fields import NoReCaptchaField

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=256)
    captcha = NoReCaptchaField()
    message = forms.CharField(
        max_length=2000,
        help_text="enter your message here; 2000 characters max",
        widget=forms.Textarea,
    )
    sender = forms.CharField(max_length=256, label="From")
    subject = forms.CharField(max_length=256)

    def send_email(self):
        try:
            msg = EmailMessage(
                subject=self.cleaned_data["subject"],
                body=self.cleaned_data["message"],
                from_email=self.cleaned_data["email"],
                to=getattr(settings, "ENVELOPE_EMAIL_RECIPIENTS", []),
                reply_to=[self.cleaned_data["email"]],
            )
            msg.send()
            return True
        except Exception as e:
            logger.exception(e)
            return False
