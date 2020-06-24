import datetime
from itertools import chain

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render 
from django.urls import reverse
from django.views.generic import DetailView, ListView

from chipy_org.apps.job_board.forms import JobPostForm, JobProfileForm, JobUserForm

from .models import JobPost


@login_required
def create_job_post(request):

    if request.method == "POST":

        job_post = JobPost(contact=request.user)
        job_post_form = JobPostForm(request.POST, instance=job_post)
        job_user_form = JobUserForm(request.POST, instance=request.user)
        job_profile_form = JobProfileForm(request.POST, instance=request.user.profile)

        if job_post_form.is_valid() and job_user_form.is_valid() and job_profile_form.is_valid():

            job_post_form.save()
            job_user_form.save()
            job_profile_form.save()

            return HttpResponseRedirect(reverse("after-submit-job-post"))

    else:
        job_post = JobPost(contact=request.user)
        job_post_form = JobPostForm(instance=job_post)
        job_user_form = JobUserForm(instance=request.user)
        job_profile_form = JobProfileForm(instance=request.user.profile)

    return render(
        request,
        "job_post_form.html",
        {
            "job_post_form": job_post_form,
            "job_user_form": job_user_form,
            "job_profile_form": job_profile_form,
        },
    )

@login_required
def update_job_post(request, pk):
    
    job_post = get_object_or_404(JobPost, pk=pk)
    
    # Make sure that the user owns this post.
    # If the use didn't create this post, they won't have permission to update it.
    if job_post.contact == request.user:  
        
        if request.method == "POST":

            job_post_form = JobPostForm(request.POST, instance=job_post)
            job_user_form = JobUserForm(request.POST, instance=request.user)
            job_profile_form = JobProfileForm(request.POST, instance=request.user.profile)

            if job_post_form.is_valid() and job_user_form.is_valid() and job_profile_form.is_valid():

                job_post_form.save()
                job_user_form.save()
                job_profile_form.save()

                return HttpResponseRedirect(reverse("after-submit-job-post"))

        else:

            job_post_form = JobPostForm(instance=job_post)
            job_user_form = JobUserForm(instance=request.user)
            job_profile_form = JobProfileForm(instance=request.user.profile)

        return render(
            request,
            "job_post_form.html",
            {
                "job_post_form": job_post_form,
                "job_user_form": job_user_form,
                "job_profile_form": job_profile_form,
            },
        )
    
    else:

        # Permission to see this page is denied since the person trying to 
        # access it isn't the correct user.
        raise PermissionDenied()


class AfterSubmitJobPost(LoginRequiredMixin, ListView):

    context_object_name = "job_posts"
    template_name = "after_submit_job_post.html"

    def get_queryset(self):
        
        job_posts = JobPost.objects.filter(contact=self.request.user)
        
        return job_posts


class JobPostList(ListView):

    context_object_name = "job_posts"
    template_name = "job_post_list.html"

    def get_queryset(self):
        # I've split these into two queries in anticipating that there might be
        # different ordering or filtering based on sponsored vs non-sponsored
        # job posts
        sponsored_job_posts = JobPost.objects.filter(
            Q(status="AP") & Q(is_sponsor=True) & Q(expiration_date__gte=datetime.datetime.now())
        ).order_by("-id")
        other_job_posts = JobPost.objects.filter(
            Q(status="AP") & Q(is_sponsor=False) & Q(expiration_date__gte=datetime.datetime.now())
        ).order_by("-id")

        # I put the two groups of job posts back together so they can processed
        # by the same loop in the template
        job_posts = list(chain(sponsored_job_posts, other_job_posts))

        return job_posts


class JobPostDetail(DetailView):
    model = JobPost
    context_object_name = "job_post"
    template_name = "job_post_detail.html"
