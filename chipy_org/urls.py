import django.contrib.auth.views
import django.views
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView

import chipy_org.apps.main.views
from chipy_org.apps.contact.views import ContactView
from chipy_org.apps.main.views import LogoutWithRedirectAndMessage
from chipy_org.apps.meetings.views import MeetingListAPIView, MeetingMeetupSync

admin.autodiscover()

urlpatterns = [
    path("", include("chipy_org.apps.main.urls")),
    path("", include("social_django.urls", namespace="social")),
    path("accounts/login/", django.contrib.auth.views.LoginView.as_view()),
    path("login/", TemplateView.as_view(template_name="login.html")),
    path("grappelli/", include("grappelli.urls")),
    path("meetings/", include("chipy_org.apps.meetings.urls")),
    path("groups/", include("chipy_org.apps.subgroups.urls")),
    path("announcements/", include("chipy_org.apps.announcements.urls")),
    path("profiles/", include("chipy_org.apps.profiles.urls")),
    path("admin/", admin.site.urls),
    path("logout/", LogoutWithRedirectAndMessage.as_view()),
    path("contact/", ContactView.as_view(), name="contact"),
    path("tinymce/", include("tinymce.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path("sponsors/", include("chipy_org.apps.sponsors.urls")),
    path("job-board/", include("chipy_org.apps.job_board.urls")),
]

# Would love a back tracking url resolver
urlpatterns += [
    path("api/meetings/", MeetingListAPIView.as_view()),
    path("api/meetings/<int:meeting_id>/meetup/sync", MeetingMeetupSync.as_view()),
]

if settings.SERVE_MEDIA:
    urlpatterns += [
        path(
            r"media/<path:path>",
            django.views.static.serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    ]
    urlpatterns += staticfiles_urlpatterns()

handler404 = chipy_org.apps.main.views.custom_404
