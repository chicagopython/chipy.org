from captcha.fields import ReCaptchaField
from django.forms import ModelForm, ModelChoiceField
from .models import Topic, Presentor, RSVP, Meeting
import datetime


class TopicForm(ModelForm):
    required = (
        'title',
        'meeting',
        'description',
    )

    meeting = ModelChoiceField(queryset=Meeting.objects.filter(when__gt=datetime.datetime.now()))

    def __init__(self, request, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = True

        self.request = request

    class Meta:
        model = Topic
        fields = (
            'title',
            'meeting',
            'length',
            'description',
            'license',
            'slides_link',
        )

    def save(self, commit=True):
        instance = super(TopicForm, self).save(commit=commit)
        if self.request and not instance.presentors.count():
            presentor, created = Presentor.objects.get_or_create(
                user=self.request.user,
                name=self.request.user.get_full_name(),
                email=self.request.user.email,
                release=True,
            )

        instance.presentors.add(presentor)
        return instance


class RSVPForm(ModelForm):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})

    def __init__(self, request, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.request = request
        if self.request.user.is_authenticated():
            # Don't need captcha for authenticated users
            del self.fields['captcha']
        else:
            # Require an email for anonymous rsvps
            self.fields['email'].required = True

    class Meta:
        model = RSVP
        fields = ('response', 'user', 'name', 'meeting', 'email')

    def clean_user(self):
        if not self.cleaned_data['user'] and self.request.user.is_authenticated():
            return self.request.user
