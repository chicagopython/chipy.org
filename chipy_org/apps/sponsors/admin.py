from django.contrib import admin
from .models import Sponsor, MeetingSponsor


class MeetingSponsorInline(admin.StackedInline):
    extra = 0 
    model = MeetingSponsor

class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", ]
    search_fields = ["name", "slug", "url"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Sponsor, SponsorAdmin)

