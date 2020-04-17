from django.contrib import admin
from .models import SubGroup


class SubGroupAdmin(admin.ModelAdmin):
    search_fields = ["name", "slug"]
    list_display = ["id", "name", "slug"]
    filter_horizontal = ["organizers"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(SubGroup, SubGroupAdmin)
