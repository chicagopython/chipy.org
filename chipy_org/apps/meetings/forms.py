import datetime

from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse

from chipy_org.libs.custom_captcha import CustomCaptchaTextInput

from .models import RSVP, Meeting, Presenter, Topic


class TopicForm(forms.ModelForm):
    required = (
        "title",
        "name",
        "email",
        "description",
        "experience_level",
        "length",
    )

    name = forms.CharField(label="Your Name", required=True)
    email = forms.EmailField(label="Your Email", required=True)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].required = True
        self.fields["experience_level"].required = True
        self.fields["length"].required = True
        self.fields["email"].initial = request.user.email
        self.fields["name"].initial = request.user.get_full_name()

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "propose_topic"
        self.helper.form_action = reverse("propose_topic")
        self.helper.add_input(Submit("submit", "Submit Topic"))

        self.request = request

    class Meta:
        model = Topic
        fields = (
            "title",
            "name",
            "email",
            "length",
            "experience_level",
            "description",
            "notes",
            "license",
            "slides_link",
        )

    def save(self, commit=True):
        instance = super().save(commit=commit)
        user = self.request.user
        if not user.email:
            user.email = self.cleaned_data.get("email")
            user.save()

        if self.request and not instance.presenters.count():
            presenter, _ = Presenter.objects.get_or_create(
                user=user,
                name=self.cleaned_data.get("name"),
                email=self.cleaned_data.get("email"),
                release=True,
            )

        instance.presenters.add(presenter)
        return instance


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
    captcha = CaptchaField(widget=CustomCaptchaTextInput)
