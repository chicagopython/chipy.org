from django.contrib import admin

from .models import JobPost


class JobPostAdmin(admin.ModelAdmin):
    list_display = ('position', 'company_name', 'created', 'status', 'status_change_date')

admin.site.register(JobPost, JobPostAdmin)

