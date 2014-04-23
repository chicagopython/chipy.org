import random
import string

from models import Meeting, Venue, Topic, Presentor, RSVP
from django.contrib import admin

from django import forms

admin.site.register(Venue)


class TopicInline(admin.StackedInline):
    model = Topic
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ('approved', 'title', 'meeting')


class MeetingForm(forms.ModelForm):
    def clean_key(self):
        if not self.cleaned_data['key']:
            return ''.join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))
        return self.cleaned_data['key']

    class Meta:
        model = Meeting


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('when','where','created','modified')
    form = MeetingForm
    inlines = [
        TopicInline,
    ]


admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Presentor)
admin.site.register(RSVP)
