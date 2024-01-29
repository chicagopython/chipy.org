import random
import string

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from chipy_org.apps.sponsors.admin import MeetingSponsorInline

from .models import RSVP, Meeting, MeetingType, Presenter, Topic, Venue


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address"]
    search_fields = ["name", "email", "phone", "address"]
    readonly_fields = ["created", "modified"]


class TopicInline(admin.StackedInline):
    model = Topic
    filter_horizontal = ["presenters"]
    readonly_fields = [
        "modified",
        "created",
    ]
    extra = 0


class CustomTopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget = CKEditorWidget()


class TopicAdmin(admin.ModelAdmin):
    form = CustomTopicForm

    list_display = (
        "id",
        "approved",
        "title",
        "experience_level",
        "get_presenters",
        "meeting",
        "created",
        "email_presenters",
    )
    readonly_fields = [
        "get_presenters",
        "modified",
        "created",
    ]
    list_filter = ["approved", "experience_level"]
    search_fields = ["title"]
    filter_horizontal = ["presenters"]

    def email_presenters(self, obj):
        presenters = obj.presenters.all()
        to_addresses = ",".join(p.email or "" for p in presenters)
        names = " and ".join(p.name or "" for p in presenters)
        title = (obj.title or "").replace("&", "")
        body = "".join(
            [f"Greetings {names},%0A%0A", "Thanks for submitting your talk: ", obj.title]
        )

        return format_html(
            f"<a href='mailto:{to_addresses}?subject=Speaking at ChiPy - {title}&body={body}'>Email Presenters</a>"
        )

    def get_presenters(self, obj):
        return format_html(
            " &bull; ".join(
                [
                    f"<a href='{reverse('admin:meetings_presenter_change', args=[p.id])}'>"
                    f"{p.name}</a>"
                    for p in obj.presenters.all()
                ]
            )
        )

    get_presenters.short_description = "Presenter Links"


class MeetingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["meetup_id"].widget = admin.widgets.AdminTextInputWidget()

    def clean_key(self):
        if not self.cleaned_data["key"]:
            return "".join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))
        return self.cleaned_data["key"]

    class Meta:
        model = Meeting
        exclude = []  # pylint: disable=modelform-uses-exclude


class MeetingAdmin(admin.ModelAdmin):
    list_display = ["title", "meeting_type", "when", "where", "created", "modified", "action"]
    list_filter = ["meeting_type"]
    form = MeetingForm
    inlines = [
        TopicInline,
        MeetingSponsorInline,
    ]
    readonly_fields = ["created", "modified", "presenter_mailboxes"]

    @admin.display(description="Presenter Emails")
    def presenter_mailboxes(self, obj):
        return ', '.join(obj.get_presenter_mailboxes())

    @mark_safe
    def action(self, obj):
        if obj.meetup_id:
            return f"""
                <input
                    type="submit"
                    value="Sync Meetup"
                    class="meetup-sync-button"
                    data-meeting-pk="{obj.pk}"
                >
                """
        return ""

    class Media:
        js = [
            "admin/js/jquery.init.js",
            "js/meetup_sync.js",
        ]

    ordering = ("-when",)


class PresenterAdmin(admin.ModelAdmin):
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
        "status",
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
    list_filter = [
        "response",
        "status",
    ]


class MeetingTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Venue, VenueAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(RSVP, RSVPAdmin)
admin.site.register(MeetingType, MeetingTypeAdmin)
