from django.contrib import admin

from .models import CustomFlatPage


@admin.register(CustomFlatPage)
class CustomFlatPageAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "header_image")
    search_fields = ("title", "url")
