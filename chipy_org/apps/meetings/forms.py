from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse
from django_recaptcha.fields import ReCaptchaField

from chipy_org.libs.custom_captcha import CrispyReCaptchaV2Checkbox
from .models import RSVP


class RSVPForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["email", "first_name", "last_name"]:
            self.fields[field].required = True

        if self.instance.pk:
            del self.fields["email"]

        meeting = kwargs.get("initial").get("meeting", None)
        if meeting:
            if not meeting.is_in_person():
                choices = [(i, j) for i, j in self.fields["response"].choices if j != "in-person"]
                self.fields["response"] = forms.ChoiceField(choices=choices)

            if not meeting.is_virtual():
                choices = [(i, j) for i, j in self.fields["response"].choices if j != "virtual"]
                self.fields["response"] = forms.ChoiceField(choices=choices)

        self.helper = FormHelper()
        self.helper.form_id = "rsvp-form"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("rsvp")
        self.helper.add_input(Submit("submit", "RSVP"))

    class Meta:
        model = RSVP
        fields = (
            "user",
            "response",
            "meeting",
            "first_name",
            "last_name",
            "email",
        )
        labels = {
            "first_name": "First name on your legal ID",
            "last_name": "Last name on your legal ID",
        }
        widgets = {
            "meeting": forms.HiddenInput(),
            "user": forms.HiddenInput(),
        }

    def clean_first_name(self):
        return self.cleaned_data["first_name"].lower()

    def clean_last_name(self):
        return self.cleaned_data["last_name"].lower()

    def clean_email(self):
        return self.cleaned_data["email"].lower()


class RSVPFormWithCaptcha(RSVPForm):
    captcha = ReCaptchaField(widget=CrispyReCaptchaV2Checkbox, label="")
