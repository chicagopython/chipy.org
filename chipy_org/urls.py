import django.contrib.auth.views
import django.views
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

import chipy_org.apps.main.views
from chipy_org.apps.contact.views import ChipyContactView
from chipy_org.apps.meetings.views import MeetingListAPIView, MeetingMeetupSync

admin.autodiscover()

urlpatterns = [
    url(r"", include("chipy_org.apps.main.urls")),
    url("", include("social_django.urls", namespace="social")),
    url(r"^accounts/login/$", django.contrib.auth.views.LoginView.as_view()),
    url(r"^login/{0,1}$", TemplateView.as_view(template_name="login.html")),
    url(r"^grappelli/", include("grappelli.urls")),
    url(r"^meetings/", include("chipy_org.apps.meetings.urls")),
    url(r"^groups/", include("chipy_org.apps.subgroups.urls")),
    url(r"^announcements/", include("chipy_org.apps.announcements.urls")),
    url(r"^profiles/", include("chipy_org.apps.profiles.urls")),
    url(r"^admin/", admin.site.urls),
    url(r"^about/", include("chipy_org.apps.about.urls")),
    url(r"^logout", django.contrib.auth.views.LogoutView.as_view(), {"next_page": "/"}),
    url(r"^contact/", ChipyContactView.as_view(), name="contact"),
    url(r"^tinymce/", include("tinymce.urls")),
    url(r"^pages/", include("django.contrib.flatpages.urls")),
    url(r"^sponsors/", include("chipy_org.apps.sponsors.urls")),
    url(r"^job/", include("chipy_org.apps.job_board.urls")),
]

# Would love a back tracking url resolver
urlpatterns += [
    url(r"^api/meetings/$", MeetingListAPIView.as_view()),
    url(r"^api/meetings/(?P<meeting_id>\d+)/meetup/sync$", MeetingMeetupSync.as_view()),
]

if settings.SERVE_MEDIA:
    urlpatterns += [
        url(
            r"^media/(?P<path>.*)$",
            django.views.static.serve,
            {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
        ),
    ]
    urlpatterns += staticfiles_urlpatterns()

handler404 = chipy_org.apps.main.views.customer_404
