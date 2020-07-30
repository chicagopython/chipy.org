from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea

from chipy_org.apps.profiles.models import UserProfile

from .models import JobPost


class JobPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobPostForm, self).__init__(*args, **kwargs)
        self.fields["agree_to_terms"].required = True

    class Meta:
        model = JobPost

        fields = [
            "company_name",
            "position",
            "job_type",
            "location",
            "description",
            "is_sponsor",
            "can_host_meeting",
            "company_website",
            "how_to_apply",
            "agree_to_terms",
        ]

        widgets = {
            "description": Textarea(attrs={"cols": 60, "rows": 20, "placeholder": "2500 Character Limit"}),
            "contact": forms.HiddenInput(),
            "how_to_apply": Textarea(attrs={"cols": 60, "rows": 20}),
        }


class JobUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(JobUserForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    class Meta:
        model = User

        fields = ["first_name", "last_name", "email"]


class JobProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

        fields = ["is_external_recruiter"]
