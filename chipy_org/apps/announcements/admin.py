from django.contrib import admin
from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["id", "active", "end_date", "headline", "created"]
    search_fields = [
        "id",
        "headline",
        "body",
    ]
    readonly_fields = ["created", "modified"]
    list_filter = ["active"]


admin.site.register(Announcement, AnnouncementAdmin)
