from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.urls import reverse

from ..meetings.models import Presenter, Topic


class TopicForm(forms.ModelForm):
    required = (
        "title",
        "name",
        "email",
        "phone",
        "description",
        "experience_level",
        "length",
    )

    name = forms.CharField(label="Your Name", required=True)
    email = forms.EmailField(label="Your Email", required=True)
    phone = forms.CharField(
        label="Your Phone",
        required=True,
        help_text="In case we need to reach you the day of the event.",
    )

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
            "phone",
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
                phone=self.cleaned_data.get("phone"),
                release=True,
            )

        instance.presenters.add(presenter)
        return instance
