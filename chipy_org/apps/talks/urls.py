from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import MyTopics, PastTopic, PastTopics, ProposeTopic

urlpatterns = [
    path("topics/propose/", login_required(ProposeTopic.as_view()), name="propose_topic"),
    path("topics/mine/", login_required(MyTopics.as_view()), name="my_topics"),
    path("topics/past/", PastTopics.as_view(), name="past_topics"),
    path("topics/past/<int:id>/", PastTopic.as_view(), name="past_topic"),
]
