from django.conf.urls import url

from .views import GroupDetail

urlpatterns = [
    url(r"^(?P<slug>[a-zA-Z0-9\-\_]*)/$", GroupDetail.as_view(), name="groups"),
]
