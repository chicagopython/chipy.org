from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

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
    url(r"^$", FutureMeetings.as_view(), name="future_meetings"),
    url(r"^admin_tools/", include("admin_tools.urls")),
    url(r"^ical/$", MeetingFeed(), name="ical_feed"),
    url(r"^past/$", PastMeetings.as_view(), name="past_meetings"),
    url(r"^(?P<pk>[0-9]*)/$", MeetingDetail.as_view(), name="meeting"),
    url(r"^rsvp/$", RSVP.as_view(), name="rsvp"),
    url(r"^rsvp/(?P<rsvp_key>[a-z0-9]{40})/$", UpdateRSVP.as_view(), name="update_rsvp_with_key"),
    url(
        r"^rsvp/list/(?P<meeting_key>[a-z0-9]{40})/private.csv$",
        RSVPlistPrivate.as_view(),
        name="rsvp_list_csv",
    ),
    url(
        r"^rsvp/list/(?P<meeting_key>[a-z0-9]{40})/host.csv$",
        RSVPlistHost.as_view(),
        name="rsvp_list_host_csv",
    ),
    url(r"^topics/propose/$", login_required(ProposeTopic.as_view()), name="propose_topic"),
    url(r"^topics/mine/$", login_required(MyTopics.as_view()), name="my_topics"),
    url(r"^topics/past/$", PastTopics.as_view(), name="past_topics"),
    url(r"^topics/past/(?P<id>\d+)/$", PastTopic.as_view(), name="past_topic"),
    url(r"^upcoming_events/", UpcomingEvents.as_view(), name="upcoming_events"),
]
