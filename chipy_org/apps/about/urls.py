from django.conf.urls import url


urlpatterns = [
    url(r"^$", 'django.contrib.flatpages.views.flatpage',
        {'url': '/about/'}, name='about'),
]
