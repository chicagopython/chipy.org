from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from chipy_org.apps.job_board.forms import JobPostForm, JobUserForm, JobProfileForm
from django.contrib.auth.decorators import login_required
from .models import JobPost
from django.db.models import Q
from itertools import chain
import datetime


@login_required
def create_job_post(request):

    if request.method == "POST":

        job_post_form = JobPostForm(request.POST)
        job_user_form = JobUserForm(request.POST, instance=request.user)
        job_profile_form = JobProfileForm(request.POST, instance=request.user.profile)

        if job_post_form.is_valid() and job_user_form.is_valid() and job_profile_form.is_valid():

            job_post_form.save()
            job_user_form.save()
            job_profile_form.save()

            return HttpResponseRedirect(reverse("after-submit-job-post"))

    else:
        job_post_form = JobPostForm(
            initial={"contact": request.user}
        )  # sets an intial value only for unbound form, not for bound form
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


def after_submit_job_post(request):

    return render(request, "after_submit_job_post.html", {})


class JobPostList(ListView):

    context_object_name = "job_posts"
    template_name = "job_post_list.html"

    def get_queryset(self):
        # I've split these into two queries in anticipating that there might be different ordering or filtering based on sponsored vs non-sponsored job posts
        sponsored_job_posts = JobPost.objects.filter(
            Q(status="AP") & Q(is_sponsor=True) & Q(expiration_date__gte=datetime.datetime.now())
        ).order_by("-id")
        other_job_posts = JobPost.objects.filter(
            Q(status="AP") & Q(is_sponsor=False) & Q(expiration_date__gte=datetime.datetime.now())
        ).order_by("-id")

        # I put the two groups of job posts back together so they can processed by the same loop in the template
        job_posts = list(chain(sponsored_job_posts, other_job_posts))

        return job_posts


class JobPostDetail(DetailView):
    model = JobPost
    context_object_name = "job_post"
    template_name = "job_post_detail.html"
