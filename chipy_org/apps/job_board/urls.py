from django.urls import path

from .views import AfterSubmitJobPost, JobPostDetail, JobPostList, create_job_post, update_job_post

urlpatterns = [
    path(r"create/", create_job_post, name="create-job-post"),
    path(r"update/<int:pk>/", update_job_post, name='update-job-post'),
    path(r"list/", JobPostList.as_view(), name="job-post-list"),
    path(r"detail/<int:pk>/", JobPostDetail.as_view(), name="job-post-detail"),
    path(r"after-submit/", AfterSubmitJobPost.as_view(), name="after-submit-job-post"),   
]