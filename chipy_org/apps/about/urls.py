from django.conf.urls import patterns, url

urlpatterns = [
    url(r"^$", 'django.contrib.flatpages.views.flatpage',
        {'url': '/about/'}, name='about'),
]
