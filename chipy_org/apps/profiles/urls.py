from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from profiles.views import (ProfilesList,
                            ProfileEdit,
)

urlpatterns = patterns("",
    url(r'^list/$', ProfilesList.as_view(), name='list'),
    url(r'^edit/$', ProfileEdit.as_view(), name='edit'),
)
