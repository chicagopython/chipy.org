from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path

from .feeds import MeetingFeed
from .views import (
    RSVP,
    FutureMeetings,
    MeetingDetail,
    MyTopics,
    PastMeetings,
    PastTopic,
    PastTopics,
    ProposeTopic,
    RSVPlistHost,
    RSVPlistPrivate,
    UpcomingEvents,
    UpdateRSVP,
)

urlpatterns = [
    path("", FutureMeetings.as_view(), name="future_meetings"),
    path("admin_tools/", include("admin_tools.urls")),
    path("ical/", MeetingFeed(), name="ical_feed"),
    path("past/", PastMeetings.as_view(), name="past_meetings"),
    path("<int:pk>/", MeetingDetail.as_view(), name="meeting"),
    path("rsvp/", RSVP.as_view(), name="rsvp"),
    re_path(r"rsvp/(?P<rsvp_key>[a-z0-9]{40})/", UpdateRSVP.as_view(), name="update_rsvp_with_key"),
    re_path(
        r"rsvp/list/(?P<meeting_key>[a-z0-9]{40})/private.csv",
        RSVPlistPrivate.as_view(),
        name="rsvp_list_csv",
    ),
    re_path(
        r"rsvp/list/(?P<meeting_key>[a-z0-9]{40})/host.csv",
        RSVPlistHost.as_view(),
        name="rsvp_list_host_csv",
    ),
    path("topics/propose/", login_required(ProposeTopic.as_view()), name="propose_topic"),
    path("topics/mine/", login_required(MyTopics.as_view()), name="my_topics"),
    path("topics/past/", PastTopics.as_view(), name="past_topics"),
    path("topics/past/<int:id>/", PastTopic.as_view(), name="past_topic"),
    path("upcoming_events/", UpcomingEvents.as_view(), name="upcoming_events"),
]
