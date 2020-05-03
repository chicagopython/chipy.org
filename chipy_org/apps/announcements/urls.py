from django.conf.urls import url

from .views import AnnouncementsList

urlpatterns = [
    url(r"^$", AnnouncementsList.as_view(), name="announcements_list"),
]
