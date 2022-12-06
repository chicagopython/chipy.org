from django.urls import path

from .views import JoinSlackView

urlpatterns = [
    path("join", JoinSlackView.as_view(), name="join_slack"),
]
