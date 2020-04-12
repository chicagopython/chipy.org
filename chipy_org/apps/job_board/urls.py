from django.conf.urls import url
#from django.urls import path
from .views import create_job_post, thanks, job_post_list, job_post_detail

urlpatterns = [
    url(r'^create-job-post/$', create_job_post, name='create-job-post'),
    url(r'^job-post-list/$', job_post_list, name='job-post-list'),
    url(r'^job-post-detail/(?P<pk>\d+)/$', job_post_detail, name='job-post-detail'),
    url(r'^thanks/$', thanks, name='thanks'),

    # Can't use 'path' until Django 2.0, We are currently on Django 1.11.28
    #path(r'^job-post-detail/<int:pk>/$', job_post_detail, name='job-post-detail'),

]