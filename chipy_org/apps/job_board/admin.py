from django import forms
from django.contrib import admin

from .models import Affiliation, JobPost


class JobPostAdmin(admin.ModelAdmin):

    list_display = (
        "position",
        "id",
        "company_name",
        "is_sponsor",
        "created",
        "status",
        "approval_date",
        "expiration_date",
    )

    # Substitute the CharField Widget for a TextArea Widget.
    # This is used for the 'description' and 'how_to_apply' CharField in the admin
    def formfield_for_dbfield(self, db_field, **kwargs):  # pylint: disable=arguments-differ
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in {"description", "how_to_apply"}:
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Affiliation)
