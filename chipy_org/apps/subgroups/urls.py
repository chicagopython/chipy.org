from django.urls import path

from .views import GroupDetail

urlpatterns = [
    path("<slug:slug>/", GroupDetail.as_view(), name="groups"),
]
