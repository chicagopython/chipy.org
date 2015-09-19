from django.conf.urls import *
from .views import SponsorDetailView


urlpatterns = patterns("",
    url(r'^detail/(?P<slug>[\w]+)/$',
        SponsorDetailView.as_view(), name='sponsor_detail'),
)
