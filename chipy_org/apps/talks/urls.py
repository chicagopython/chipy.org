from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import (MyTopics, PastTopic, PastTopics, PastVideoTopics,
                    PendingTopics, ProposeTopic)

urlpatterns = [
    path("topics/propose/", login_required(ProposeTopic.as_view()), name="propose_topic"),
    path("topics/mine/", login_required(MyTopics.as_view()), name="my_topics"),
    path("topics/past/", PastTopics.as_view(), name="past_topics"),
    path("topics/pending/", staff_member_required(PendingTopics.as_view()), name="pending_topics"),
    path("topics/videos/", PastVideoTopics.as_view(), name="past_video_topics"),
    path("topics/past/<int:id>/", PastTopic.as_view(), name="past_topic"),
]
