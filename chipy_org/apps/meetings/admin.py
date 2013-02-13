from models import Meeting, Venue, Topic, Presentor, RSVP
from django.contrib import admin

admin.site.register(Venue)

class MeetingAdmin(admin.ModelAdmin):
    list_display = ('when','where','created','modified')
    exclude = [
    ]
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Topic)
admin.site.register(Presentor)
admin.site.register(RSVP)
