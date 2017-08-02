from django.views.generic import ListView
from .models import Announcement


class AnnouncementsList(ListView):
    template_name = 'announcements/past_announcements.html'
    queryset = Announcement.objects.filter().order_by("-created")
    context_object_name = "announcements"
