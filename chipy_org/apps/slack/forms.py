import logging

import requests
from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.conf import settings
from django.contrib import messages
from django.forms import ValidationError

from chipy_org.libs.custom_captcha import CustomCaptchaTextInput

SLACK_INVITE_API_URL = f"{settings.SLACK_URL}/api/users.admin.invite"

logger = logging.getLogger()


logger = logging.getLogger(__name__)


class SlackSignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Signup for Slack"))

    email = forms.EmailField(max_length=256)
    captcha = CaptchaField(widget=CustomCaptchaTextInput)

    def clean_email(self):
        result = requests.post(
            SLACK_INVITE_API_URL,
            data={
                "email": self.cleaned_data["email"],
                "token": settings.SLACK_TOKEN,
                "set_active": True,
            },
        )

        obj = result.json()

        if obj.get("error") == "already_invited":
            raise ValidationError(
                "You have already been invited, please check email", code="already_invited"
            )
        if obj.get("error") == "already_in_team":
            raise ValidationError("You are already in the team", code="already_in_team")
        if obj.get("error"):
            logger.error("Unxpected error during slack signup: %s", obj.get("error"))
            raise ValidationError("Unexpected error, please contact administrators", code="unknown")

        return obj["ok"] is True
