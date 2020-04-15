from django.conf.urls import url
#from django.urls import path
from .views import create_job_post, after_submit_job_post, job_post_list, job_post_detail

urlpatterns = [
    url(r'^create/$', create_job_post, name='create-job-post'),
    url(r'^list/$', job_post_list, name='job-post-list'),
    url(r'^detail/(?P<pk>\d+)/$', job_post_detail, name='job-post-detail'),
    url(r'^after-submit/$', after_submit_job_post, name='after-submit-job-post'),

    # Can't use 'path' until Django 2.0, We are currently on Django 1.11.28
    #path(r'^job-post-detail/<int:pk>/$', job_post_detail, name='job-post-detail'),

]