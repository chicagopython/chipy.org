import logging

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from nocaptcha_recaptcha.fields import NoReCaptchaField

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].label = ""
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Send Email"))

    sender = forms.CharField(max_length=256, label="From")
    email = forms.EmailField(max_length=256)
    subject = forms.CharField(max_length=256)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs=dict(cols=19, rows=10, placeholder="2000 character limit")),
    )
    captcha = NoReCaptchaField()

    def send_email(self):
        msg = EmailMessage(
            subject=self.cleaned_data["subject"],
            body=self.cleaned_data["message"],
            from_email=self.cleaned_data["email"],
            to=getattr(settings, "ENVELOPE_EMAIL_RECIPIENTS", []),
            reply_to=[self.cleaned_data["email"]],
        )
        msg.send()
