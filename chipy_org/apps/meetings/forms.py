import datetime

from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .models import RSVP, Meeting, Presentor, Topic


class TopicForm(forms.ModelForm):
    required = (
        "title",
        "name",
        "email",
        "description",
        "experience_level",
        "length",
    )

    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.filter(when__gt=datetime.datetime.now())
    )
    name = forms.CharField(label="Your Name", required=True)
    email = forms.EmailField(label="Your Email", required=True)

    def __init__(self, request, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields["meeting"].required = False
        self.fields["description"].required = True
        self.fields["experience_level"].required = True
        self.fields["length"].required = True
        self.fields["email"].initial = request.user.email
        self.fields["name"].initial = request.user.get_full_name()

        self.request = request

    class Meta:
        model = Topic
        fields = (
            "title",
            "name",
            "email",
            "meeting",
            "length",
            "experience_level",
            "description",
            "notes",
            "license",
            "slides_link",
        )

    def save(self, commit=True):
        instance = super(TopicForm, self).save(commit=commit)
        user = self.request.user
        if not user.email:
            user.email = self.cleaned_data.get("email")
            user.save()

        if self.request and not instance.presentors.count():
            presenter, _ = Presentor.objects.get_or_create(
                user=user,
                name=self.cleaned_data.get("name"),
                email=self.cleaned_data.get("email"),
                release=True,
            )

        instance.presentors.add(presenter)
        return instance


class RSVPForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ["email", "first_name", "last_name"]:
            self.fields[field].required = True

        if self.instance.pk:
            del self.fields["email"]

    class Meta:
        model = RSVP
        fields = ("user", "response", "meeting", "first_name", "last_name", "email")
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
    captcha = NoReCaptchaField()

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["captcha"].label = ""
