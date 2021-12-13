from django.urls import path

from .views import AnnouncementsList

urlpatterns = [
    path("", AnnouncementsList.as_view(), name="announcements_list"),
]
