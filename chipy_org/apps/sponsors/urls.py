from django.urls import path

from .views import SponsorDetailView, SponsorListView

urlpatterns = [
    path("detail/<slug:slug>/", SponsorDetailView.as_view(), name="sponsor_detail"),
    path("list/", SponsorListView.as_view(), name="sponsor_list"),
]
