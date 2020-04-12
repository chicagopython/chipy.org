from django.conf.urls import url
from .views import create_job_post, thanks, job_post_list

urlpatterns = [
    url(r'^create-job-post/$', create_job_post, name='create-job-post'),
    url(r'^job-post-list/$', job_post_list, name='job-post-list'),
    url(r'^thanks/$', thanks, name='thanks'),
]