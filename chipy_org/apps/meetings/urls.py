from django.conf.urls.defaults import *
from meetings.views import *

urlpatterns = patterns("",
    url(r'^past/$', PastMeetings.as_view(), name='past_meetings'),
    url(r'^topic/propose$', ProposeTopic.as_view(), name='propose_topic'),

)
