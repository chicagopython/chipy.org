import random
import string

from django.contrib import admin
from django.contrib.admin import widgets
from django import forms

from models import Meeting, Venue, Topic, Presentor, RSVP

admin.site.register(Venue)


class TopicInline(admin.StackedInline):
    model = Topic
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = ('approved', 'title', 'meeting')


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        self.fields['meetup_id'].widget = admin.widgets.AdminTextInputWidget()

    def clean_key(self):
        if not self.cleaned_data['key']:
            return ''.join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))
        return self.cleaned_data['key']

    class Meta:
        model = Meeting


class MeetingAdmin(admin.ModelAdmin):
    list_display = ('when', 'where', 'created', 'modified', 'action')
    form = MeetingForm
    inlines = [
        TopicInline,
    ]

    def action(self, obj):
        if obj.meetup_id:
            return '<input type="submit" value="Sync Meetup" class="meetup-sync-button" data-meeting-pk="{}">'.format(
                obj.pk)
        return ''

    action.allow_tags = True

    class Media:
        js = ("js/meetup_sync.js",)

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Presentor)
admin.site.register(RSVP)
