from django.conf.urls import url
from django.contrib.flatpages.views import flatpage


urlpatterns = [
    url(r"^$", flatpage, {"url": "/about/"}, name="about"),
]
