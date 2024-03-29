from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import ProfileEdit, ProfilesList, ProfilesListOrganizers

app_name = "profiles"  # pylint: disable=invalid-name

urlpatterns = [
    path("list/", ProfilesList.as_view(), name="list"),
    path("edit/", login_required(ProfileEdit.as_view()), name="edit"),
    path("list/organizers", ProfilesListOrganizers.as_view(), name="organizers"),
]
