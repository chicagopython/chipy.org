import random
import string
from django.contrib import admin
from django import forms
from django.shortcuts import get_object_or_404
from django.urls import reverse, path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse
from django.contrib.admin.utils import unquote
from django.contrib import messages
from django.shortcuts import redirect
from chipy_org.apps.sponsors.admin import MeetingSponsorInline
from .models import Meeting, Venue, Topic, TopicDraft, Presentor, RSVP, MeetingType
from .forms import TopicDraftFrom


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
        'drafts',
    ]
    extra = 0

    def drafts(self, instance):
        draft_count = instance.outstanding().count()
        draft_url = reverse('admin:topic_drafts', args=(instance.pk, ))
        return mark_safe("<a style='color: red' href='{}'>{}</a>".format(draft_url, draft_count))

    # short_description functions like a model field's verbose_name
    drafts.short_description = "Drafts"


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

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "<path:object_id>/drafts/",
                self.admin_site.admin_view(self.topic_drafts),
                name="topic_drafts",
            ),
            path(
                "<path:object_id>/drafts/<int:draft_id>/",
                self.admin_site.admin_view(self.topic_draft),
                name="topic_draft",
            ),
        ]
        return my_urls + urls

    def topic_drafts(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        opts = self.model._meta
        app_label = opts.app_label
        drafts = obj.drafts.filter().order_by("-created")
        context = {
            **self.admin_site.each_context(request),
            "object_id": object_id,
            "original": obj,
            "drafts": drafts,
            "app_label": app_label,
            "opts": opts,
        }
        return TemplateResponse(request, "admin/meetings/topic/topicdrafts.html", context)

    def topic_draft(self, request, object_id, draft_id):
        obj = self.get_object(request, unquote(object_id))
        opts = self.model._meta
        app_label = opts.app_label
        draft = get_object_or_404(TopicDraft, topic=obj, id=draft_id)

        if request.method == "POST":
            form = TopicDraftFrom(instance=draft, data=request.POST)
            if request.POST.get("_save"):
                form.save()
                messages.success(request, "Draft saved.")
                return redirect(request.get_full_path())
            elif request.POST.get("_publish"):
                draft = form.save(commit=False)
                draft.approved = True
                draft.save()
                draft.publish()
                messages.success(request, "Draft published.")
                return redirect(reverse("admin:meetings_topic_change", args=(obj.pk,)))
        else:
            form = TopicDraftFrom(instance=draft)

        context = {
            **self.admin_site.each_context(request),
            "object_id": object_id,
            "original": obj,
            "draft": draft,
            "app_label": app_label,
            "opts": opts,
            "form": form,
        }
        return TemplateResponse(request, "admin/meetings/topic/topicdraft.html", context)

    def get_presenters(self, obj):
        return format_html(
            " &bull; ".join(
                [
                    f"<a href='{reverse('admin:meetings_presentor_change', args=[p.id])}'>"
                    f"{p.name}</a>"
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
