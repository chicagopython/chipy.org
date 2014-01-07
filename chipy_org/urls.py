from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from apps.contact.views import ChipyContactView
from apps.meetings.views import MeetingListAPIView

admin.autodiscover()

urlpatterns = patterns(
    "",
    url(r'', include('main.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/{0,1}$',  direct_to_template, {
        'template': 'login.html'
    }),
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
    url(r'^api/meetings/', MeetingListAPIView.as_view()),
)

if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    urlpatterns += staticfiles_urlpatterns()
