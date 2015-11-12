from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import TemplateView

from chipy_org.apps.contact.views import ChipyContactView
from chipy_org.apps.meetings.views import MeetingListAPIView, MeetingMeetupSync

admin.autodiscover()

urlpatterns = patterns(
    "",
    url(r'', include('main.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/{0,1}$', TemplateView.as_view(template_name='login.html')),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^meetings/', include('meetings.urls')),
    url(r'^profiles/', include('profiles.urls', namespace="profiles")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', include('about.urls')),
    url(r'^logout', 'django.contrib.auth.views.logout',
        {'next_page': '/'}
    ),
    url(r'^contact/', ChipyContactView.as_view(), name="contact"),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
)

# Would love a back tracking url resolver
urlpatterns += patterns(
    "",
    url(r'^api/meetings/$', MeetingListAPIView.as_view()),
    url(r'^api/meetings/(?P<meeting_id>\d+)/meetup/sync$', MeetingMeetupSync.as_view())
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    urlpatterns += staticfiles_urlpatterns()
