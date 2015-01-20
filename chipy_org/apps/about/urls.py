from django.conf.urls import patterns, url

urlpatterns = patterns("",
    url(r"^$", 'django.contrib.flatpages.views.flatpage', {'url': '/about/'}, name='about'),
)
