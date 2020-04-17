from django.contrib import admin
from django import forms
from .models import JobPost


class JobPostAdmin(admin.ModelAdmin):

    list_display = (
        "position",
        "company_name",
        "is_sponsor",
        "created",
        "status",
        "approval_date",
        "expiration_date",
        "days_to_expire",
    )

    # readonly_fields = ('status_change_date')

    # Substitute the CharField Widget for a TextArea Widget.
    # This is used for the 'description' CharField in the admin
    def formfield_for_dbfield(self, db_field, _, **kwargs):
        formfield = super(JobPostAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "description":
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


admin.site.register(JobPost, JobPostAdmin)
