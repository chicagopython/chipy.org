import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from chipy_org.apps.job_board.forms import JobPostForm, JobUserForm

from .email import (
    send_email_to_admin_after_create_job_post,
    send_email_to_admin_after_user_deletes_job_post,
)
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

            position = job_post_form.cleaned_data["position"]
            company = job_post_form.cleaned_data["company_name"]
            recipients = getattr(settings, "CHICAGO_ORGANIZER_EMAILS", [])

            send_email_to_admin_after_create_job_post(position, company, recipients)

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
                    "2. In the top main menu, click on 'my jobs'.\n"
                    "3. It will take you to this page."
                ),
            )

            return HttpResponseRedirect(reverse("after-submit-job-post"))

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
                messages.success(request, "Your job post has been successfully updated.")
                return HttpResponseRedirect(reverse("after-submit-job-post"))

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
            # If the user deletes the job post before the admin approves/rejects it, send an
            # email to the admin telling them this.
            if job_post.status == "SU":
                position = job_post.position
                company = job_post.company_name
                recipients = getattr(settings, "CHICAGO_ORGANIZER_EMAILS", [])
                send_email_to_admin_after_user_deletes_job_post(position, company, recipients)

            if "delete" in request.POST:
                job_post.delete()
                messages.success(request, "Your job post has been successfully deleted.")

            else:
                messages.info(request, "The job post was not deleted.")

            return HttpResponseRedirect(reverse("after-submit-job-post"))

        else:

            return render(request, "job_board/delete_job_post.html", {"job_post": job_post})

    else:

        # Permission to see this page is denied since the person trying to
        # access it isn't the correct user.
        raise PermissionDenied()


class AfterSubmitJobPost(LoginRequiredMixin, ListView):

    model = JobPost
    context_object_name = "job_posts"
    template_name = "job_board/after_submit_job_post.html"
    paginate_by = 6

    def get_queryset(self):
        job_posts = JobPost.objects.filter(contact=self.request.user).order_by("-created")
        return job_posts


class JobPostList(ListView):
    model = JobPost
    context_object_name = "job_posts"
    template_name = "job_board/job_post_list.html"
    ordering = ("-is_sponsor", "-approval_date")
    paginate_by = 8
    queryset = JobPost.approved_and_active


class JobPostDetail(DetailView):
    model = JobPost
    context_object_name = "job_post"
    template_name = "job_board/job_post_detail.html"

    def get(self, request, *args, **kwargs):
        # Override the get method to make sure that a post
        # only gets shown if it's been approved and hasn't expired.

        pk = self.kwargs["pk"]  # pylint: disable=invalid-name
        job_post = get_object_or_404(JobPost, pk=pk)
        current_datetime = datetime.datetime.now()

        # If the post was approved and the current date is less than
        # the expiration date, then show the job post.
        if job_post.status == "AP" and (current_datetime <= job_post.expiration_date):
            return super().get(request, *args, **kwargs)
        else:
            raise Http404("Post doesn't have a status of 'approved' OR it has expired.")
