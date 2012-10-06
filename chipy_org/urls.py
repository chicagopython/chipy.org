from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns("",
    url(r'', include('main.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^login/$',  direct_to_template, {
        'template': 'login.html'
    }),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^meetings/', include('meetings.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', include('about.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
                          {'next_page': '/'}),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
    urlpatterns += staticfiles_urlpatterns()
