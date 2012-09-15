from django.conf.urls.defaults import *
from meetings.views import *

urlpatterns = patterns("",
    url(r'^past/$', PastMeetings.as_view(), name='past_meetings'),
)
