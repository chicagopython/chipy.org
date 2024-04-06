from django.urls import include, path, re_path

from .feeds import MeetingFeed
from .views import (
    RSVP,
    FutureMeetings,
    MeetingDetail,
    MeetingStatus,
    PastMeetings,
    RSVPlistHost,
    RSVPlistPrivate,
    UpcomingEvents,
    UpdateRSVP,
)

urlpatterns = [
    path("", FutureMeetings.as_view(), name="future_meetings"),
    path("admin_tools/", include("admin_tools.urls")),
    path("status/", MeetingStatus.as_view(), name="meeting_status"),
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
    path("upcoming_events/", UpcomingEvents.as_view(), name="upcoming_events"),
]
