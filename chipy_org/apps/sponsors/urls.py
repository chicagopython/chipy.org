from django.conf.urls import url
from .views import SponsorDetailView, SponsorListView


urlpatterns = [
    url(r"^detail/(?P<slug>[\w\-\_]+)/$", SponsorDetailView.as_view(), name="sponsor_detail"),
    url(r"^list/$", SponsorListView.as_view(), name="sponsor_list"),
]
