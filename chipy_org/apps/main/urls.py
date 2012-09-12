from django.conf.urls.defaults import *
from main.views import *

urlpatterns = patterns("main.views",
    url(r'^$', Home.as_view(), name='home'),
)
