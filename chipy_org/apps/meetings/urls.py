from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from .feeds import MeetingFeed
from .views import (
    PastMeetings,
    MeetingDetail,
    ProposeTopic,
    MyTopics,
    RSVP,
    RSVPlist,
    PastTopics,
    PastTopic,)


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^ical/$',
        MeetingFeed(), name="ical_feed"),
    url(r'^past/$',
        PastMeetings.as_view(), name='past_meetings'),

    url(r'^(?P<pk>[0-9]*)/$',
        MeetingDetail.as_view(), name='meeting'),

    url(r'^rsvp/$',
        RSVP.as_view(), name='rsvp'),
    url(r'^rsvp/anonymous/$',
        RSVP.as_view(), name='anonymous_rsvp'),
    url(r'^rsvp/anonymous/(?P<rsvp_key>[a-z0-9]{40})/$',
        RSVP.as_view(), name='anonymous_rsvp_with_key'),
    url(r'^rsvp/list/(?P<rsvp_key>[a-z0-9]{40})/$',
        RSVPlist.as_view(), name='rsvp_list'),
    url(r'^topics/propose/$',
        login_required(ProposeTopic.as_view()), name='propose_topic'),
    url(r'^topics/mine/$',
        login_required(MyTopics.as_view()), name='my_topics'),
    url(r'^topics/past/$',
        PastTopics.as_view(), name='past_topics'),
    url(r'^topics/past/(?P<id>\d+)/$',
        PastTopic.as_view(), name='past_topic'),
]
