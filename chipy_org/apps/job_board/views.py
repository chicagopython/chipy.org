import datetime
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from chipy_org.apps.job_board.forms import JobPostForm, JobUserForm

from .models import JobPost


@login_required
def create_job_post(request):

    if request.method == "POST":

        job_post = JobPost(contact=request.user)
        job_post_form = JobPostForm(request.POST, instance=job_post)
        job_user_form = JobUserForm(request.POST, instance=request.user)

        if job_post_form.is_valid() and job_user_form.is_valid():

            job_post_form.save()
            job_user_form.save()

            return HttpResponseRedirect(
                reverse("after-submit-job-post", kwargs={"action": "create"})
            )

    else:
        job_post = JobPost(contact=request.user)
        job_post_form = JobPostForm(instance=job_post)
        job_user_form = JobUserForm(instance=request.user)

    return render(
        request,
        "job_board/job_post_form.html",
        {"job_post_form": job_post_form, "job_user_form": job_user_form, "view_action": "create",},
    )


@login_required
def update_job_post(request, pk):  # pylint: disable=invalid-name

    job_post = get_object_or_404(JobPost, pk=pk)

    # Make sure that the user owns this post.
    # If the use didn't create this post, they won't have permission to update it.
    if job_post.contact == request.user:

        if request.method == "POST":

            job_post_form = JobPostForm(request.POST, instance=job_post)
            job_user_form = JobUserForm(request.POST, instance=request.user)

            if (
                job_post_form.is_valid()  # pylint: disable=bad-continuation
                and job_user_form.is_valid()  # pylint: disable=bad-continuation
            ):

                job_post_form.save()
                job_user_form.save()

                return HttpResponseRedirect(
                    reverse("after-submit-job-post", kwargs={"action": "update"})
                )

        else:

            job_post_form = JobPostForm(instance=job_post)
            job_user_form = JobUserForm(instance=request.user)

        return render(
            request,
            "job_board/job_post_form.html",
            {
                "job_post_form": job_post_form,
                "job_user_form": job_user_form,
                "view_action": "update",
            },
        )

    else:

        # Permission to see this page is denied since the person trying to
        # access it isn't the correct user.
        raise PermissionDenied()


@login_required
def delete_job_post(request, pk):  # pylint: disable=invalid-name

    job_post = get_object_or_404(JobPost, pk=pk)

    # Make sure that the user owns this post and has the right to delete it.
    if job_post.contact == request.user:

        if request.method == "POST":

            job_post.delete()
            return HttpResponseRedirect(
                reverse("after-submit-job-post", kwargs={"action": "delete"})
            )

        else:

            return render(request, "job_board/delete_job_post.html", {"job_post": job_post})

    else:

        # Permission to see this page is denied since the person trying to
        # access it isn't the correct user.
        raise PermissionDenied()


class AfterSubmitJobPost(LoginRequiredMixin, ListView):

    context_object_name = "job_posts"
    template_name = "job_board/after_submit_job_post.html"

    def get(self, request, *args, **kwargs):
        if self.kwargs["action"] == "create":

            messages.success(
                request,
                (
                    "Thank you for submitting a job posting!\n"
                    "It will have to be approved by an admin in order"
                    " to show up on the job board.\n"
                    " \n"
                    "You can check back on the decision status in the future.\n"
                    "To do so:\n"
                    "1. Log into chipy.org\n"
                    "2. In the user login dropdown menu, click on 'My Jobs'.\n"
                    "3. It will take you to this page."
                ),
            )

        elif self.kwargs["action"] == "update":

            messages.success(request, "Your job post has been successfully updated.")

        elif self.kwargs["action"] == "delete":

            messages.success(request, "Your job post has been successfully deleted.")

        elif self.kwargs["action"] != "show":
            raise Http404()

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        job_posts = JobPost.objects.filter(contact=self.request.user)
        return job_posts


class JobPostList(ListView):

    context_object_name = "job_posts"
    template_name = "job_board/job_post_list.html"

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
    template_name = "job_board/job_post_detail.html"
