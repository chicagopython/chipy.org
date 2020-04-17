import random
import string
from django.contrib import admin
from django import forms
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from chipy_org.apps.sponsors.admin import MeetingSponsorInline
from .models import Meeting, Venue, Topic, Presentor, RSVP, MeetingType


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address"]
    search_fields = ["name", "email", "phone", "address"]
    readonly_fields = ["created", "modified"]


class TopicInline(admin.StackedInline):
    model = Topic
    filter_horizontal = ["presentors"]
    readonly_fields = [
        "modified",
        "created",
    ]
    extra = 0


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "approved",
        "title",
        "experience_level",
        "get_presenters",
        "meeting",
        "created",
    )
    readonly_fields = [
        "get_presenters",
        "modified",
        "created",
    ]
    list_filter = ["approved", "experience_level"]
    search_fields = ["title"]
    filter_horizontal = ["presentors"]

    def get_presenters(self, obj):
        return format_html(
            " &bull; ".join(
                [
                    f"<a href='{reverse('admin:meetings_presentor_change', args=[p.id])}'>"
                    "{p.name}</a>"
                    for p in obj.presentors.all()
                ]
            )
        )

    get_presenters.short_description = "Presenter Links"


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)

        self.fields["meetup_id"].widget = admin.widgets.AdminTextInputWidget()

    def clean_key(self):
        if not self.cleaned_data["key"]:
            return "".join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))
        return self.cleaned_data["key"]

    class Meta:
        model = Meeting
        exclude = []


class MeetingAdmin(admin.ModelAdmin):
    list_display = ["title", "meeting_type", "when", "where", "created", "modified", "action"]
    list_filter = ["meeting_type"]
    form = MeetingForm
    inlines = [
        TopicInline,
        MeetingSponsorInline,
    ]
    readonly_fields = ["created", "modified"]

    def action(self, obj):
        if obj.meetup_id:
            return (
                '<input type="submit" value="Sync Meetup" '
                f'class="meetup-sync-button" data-meeting-pk="{obj.pk}">'
            )
        return ""

    action.allow_tags = True

    class Media:
        js = ("js/meetup_sync.js",)

    ordering = ("-when",)


class PresentorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user", "email", "phone"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "email", "phone"]
    readonly_fields = ["created", "modified"]


class RSVPAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "name",
        "first_name",
        "last_name",
        "email",
        "meeting",
        "response",
        "created",
    ]
    readonly_fields = ["created", "modified"]
    search_fields = [
        "id",
        "name",
        "first_name",
        "last_name",
        "email",
    ]
    list_filter = ["response"]


class MeetingTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Venue, VenueAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Presentor, PresentorAdmin)
admin.site.register(RSVP, RSVPAdmin)
admin.site.register(MeetingType, MeetingTypeAdmin)
