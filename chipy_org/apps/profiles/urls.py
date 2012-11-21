from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from profiles.views import (ProfilesList,)

urlpatterns = patterns("",
    url(r'^list/$', ProfilesList.as_view(), name='list'),
)
