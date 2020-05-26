import logging

from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from nocaptcha_recaptcha.fields import NoReCaptchaField

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    sender = forms.CharField(label="From")
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    captcha = NoReCaptchaField()

    def send_email(self):
        try:
            msg = EmailMessage(
                subject=self.subject,
                body=self.message,
                from_email=self.email,
                to=getattr(settings, "CHIPY_TOPIC_SUBMIT_EMAILS", []),
                reply_to=[self.email],
            )
            msg.send()
            return True
        except Exception as e:
            logger.exception(e)
            return False
