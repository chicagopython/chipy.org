from models import Meeting, Venue
from django.contrib import admin

admin.site.register(Venue)
 
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('when','where','created','modified')
    exclude = [
    ]
admin.site.register(Meeting, MeetingAdmin)



