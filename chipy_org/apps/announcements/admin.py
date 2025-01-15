from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE

from .models import Announcement


class CustomAnnoucementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        widgets = {"text": TinyMCE()}
        exclude = []

class AnnouncementAdmin(admin.ModelAdmin):
    form = CustomAnnoucementForm
    list_display = ["id", "active", "end_date", "headline", "created"]
    search_fields = [
        "id",
        "headline",
        "body",
    ]
    readonly_fields = ["created", "modified"]
    list_filter = ["active"]


admin.site.register(Announcement, AnnouncementAdmin)
