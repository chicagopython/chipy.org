from django.conf.urls import url

from .views import Home, PreviewHome

urlpatterns = [
    url(r"^$", Home.as_view(), name="home"),
    url(r"^preview/?$", PreviewHome.as_view(), name="home_preview"),
]
