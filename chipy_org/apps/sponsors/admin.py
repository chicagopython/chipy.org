from django.contrib import admin
from .models import Sponsor, MeetingSponsor, GeneralSponsor


class MeetingSponsorInline(admin.StackedInline):
    extra = 0
    model = MeetingSponsor


class GeneralSponsorAdmin(admin.ModelAdmin):
    model = GeneralSponsor
    list_display = ['sponsor', 'about_short']


class SponsorAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", ]
    search_fields = ["name", "slug", "url"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(GeneralSponsor, GeneralSponsorAdmin)
