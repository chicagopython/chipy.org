from django.conf.urls import url
from .views import create_job_post, thanks, JobPostList

urlpatterns = [
    url(r'^create-job-post/$', create_job_post, name='create-job-post'),
    url(r'^job-post-list/$', JobPostList.as_view(), name='job-post-list'),
    url(r'^thanks/$', thanks, name='thanks'),
]