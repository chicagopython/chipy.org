from django.urls import include, path

from .views import ContactView

urlpatterns = [
    path("", ContactView.as_view(), name="contact"),
]
