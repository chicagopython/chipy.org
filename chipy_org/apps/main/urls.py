from django.urls import path

from .views import Home

urlpatterns = [
    path("", Home.as_view(), name="home"),
]
