import datetime

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from ..meetings.models import Presenter, Topic
from .email import send_meeting_topic_submitted_email
from .forms import TopicForm


class MyTopics(ListView):
    template_name = "talks/my_topics.html"

    def get_queryset(self):
        try:
            presenter = Presenter.objects.filter(user=self.request.user)
        except Presenter.DoesNotExist:
            return Topic.objects.none()

        return Topic.objects.filter(presenters__in=presenter)


class PastTopics(ListView):
    context_object_name = "topics"
    template_name = "talks/past_topics.html"
    queryset = Topic.objects.filter(
        meeting__when__lt=datetime.date.today(), approved=True
    ).order_by("-meeting__when")


class PastTopic(DetailView):
    model = Topic
    template_name = "talks/past_topic.html"
    context_object_name = "topic"
    pk_url_kwarg = "id"


class ProposeTopic(CreateView):
    template_name = "talks/propose_topic.html"
    form_class = TopicForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Topic has been submitted.")
        recipients = getattr(settings, "CHIPY_TOPIC_SUBMIT_EMAILS", [])
        send_meeting_topic_submitted_email(self.object, recipients)
        return HttpResponseRedirect(self.get_success_url())
