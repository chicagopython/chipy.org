from nocaptcha_recaptcha.fields import NoReCaptchaField
from django import forms
from .models import Topic, Presentor, RSVP, Meeting
import datetime


class TopicForm(forms.ModelForm):
    required = (
        'title',
        "name",
        "email",
        'description',
        'experience_level',
    )

    meeting = forms.ModelChoiceField(
        queryset=Meeting.objects.filter(when__gt=datetime.datetime.now()))
    name = forms.CharField(label="Your Name", required=True)
    email = forms.EmailField(label="Your Email", required=True)

    def __init__(self, request, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['meeting'].required = False
        self.fields['description'].required = True
        self.fields['experience_level'].required = True
        self.fields['email'].initial = request.user.email
        self.fields['name'].initial = request.user.get_full_name()

        self.request = request

    class Meta:
        model = Topic
        fields = (
            'title',
            "name",
            "email",
            'meeting',
            'length',
            'experience_level',
            'description',
            'notes',
            'license',
            'slides_link',
        )

    def save(self, commit=True):
        instance = super(TopicForm, self).save(commit=commit)
        user = self.request.user
        if not user.email:
            user.email = self.cleaned_data.get('email')
            user.save()

        if self.request and not instance.presentors.count():
            presenter, created = Presentor.objects.get_or_create(
                user=user,
                name=self.cleaned_data.get('name'),
                email=self.cleaned_data.get('email'),
                release=True,
            )

        instance.presentors.add(presenter)
        return instance


class RSVPForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = RSVP
        fields = ('response', 'user', 'name', 'meeting', 'email')

    def clean_user(self):
        if not self.cleaned_data['user'] and self.request.user.is_authenticated():
            return self.request.user


class AnonymousRSVPForm(forms.ModelForm):
    captcha = NoReCaptchaField()

    def __init__(self, request, *args, **kwargs):
        super(AnonymousRSVPForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # On an update we don't want to make any changes to the email.
            del self.fields['email']
            del self.fields['captcha']
            del self.fields['meeting']

    class Meta:
        model = RSVP
        fields = ('response', 'meeting', 'name', 'email')
