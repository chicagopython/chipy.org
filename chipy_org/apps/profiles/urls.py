from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ProfileEdit, ProfilesList

app_name = "profiles"  # pylint: disable=invalid-name

urlpatterns = [
    url(r"^list/$", ProfilesList.as_view(), name="list"),
    url(r"^edit/$", login_required(ProfileEdit.as_view()), name="edit"),
]
