from django.conf.urls import url
from .views import create_job_post, thanks

urlpatterns = [
    url(r'^create-job-post/$', create_job_post, name='create-job-post'),
    url(r'^thanks/$', thanks, name='thanks'),
]