import abc
import csv
import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, ModelFormMixin, ProcessFormView, UpdateView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from chipy_org.apps.meetings.forms import RSVPForm, RSVPFormWithCaptcha

from .email import send_meeting_topic_submitted_email, send_rsvp_email
from .forms import RSVPForm, RSVPFormWithCaptcha, TopicForm
from .models import RSVP as RSVPModel
from .models import Meeting, Presenter, Topic
from .serializers import MeetingSerializer
from .utils import meetup_meeting_sync

logger = logging.getLogger(__name__)


class InitialRSVPMixin(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_meeting(self):
        # override this method to determine the meeting used for the rsvp
        # the function is expected to return a single Meeting object
        raise NotImplementedError("Must implement 'get_meeting'")

    def get_initial(self, meeting):
        initial = {"response": "Y"}
        initial.update({"meeting": meeting})
        if self.request.user.is_authenticated:
            user = self.request.user
            user_data = {
                "user": user,
                "email": getattr(user, "email", None),
                "first_name": getattr(user, "first_name", None),
                "last_name": getattr(user, "last_name", None),
            }
            initial.update(user_data)
        self.initial = initial

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return RSVPForm
        else:
            return RSVPFormWithCaptcha

    def get_form(self, **kwargs):
        form_class = self.get_form_class()
        return form_class(**kwargs)

    def add_extra_context(self, context):
        meeting = self.get_meeting()
        context["next_meeting"] = meeting

        if meeting:
            self.get_initial(meeting)
            context["form"] = self.get_form(request=self.request, initial=self.initial)

            if self.request.user.is_authenticated:
                context["rsvp"] = RSVPModel.objects.filter(
                    meeting=meeting, user=self.request.user
                ).first()
        return context


class FutureMeetings(ListView):
    template_name = "meetings/future_meetings.html"
    queryset = Meeting.objects.filter(
        when__gt=datetime.datetime.now() - datetime.timedelta(hours=3)
    ).order_by("when")
    paginate_by = 5


class PastMeetings(ListView):
    template_name = "meetings/past_meetings.html"
    queryset = Meeting.objects.filter(
        when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
    ).order_by("-when")
    paginate_by = 5


class MeetingDetail(DetailView, InitialRSVPMixin):
    template_name = "meetings/meeting.html"
    pk_url_kwarg = "pk"
    model = Meeting

    def get_meeting(self):
        return self.object

    def get_context_data(self, **kwargs):
        context = super(MeetingDetail, self).get_context_data(**kwargs)
        context.update(kwargs)
        context = self.add_extra_context(context)
        return context


class ProposeTopic(CreateView):
    template_name = "meetings/propose_topic.html"
    form_class = TopicForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super(ProposeTopic, self).get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Topic has been submitted.")
        recipients = getattr(settings, "CHIPY_TOPIC_SUBMIT_EMAILS", [])
        send_meeting_topic_submitted_email(self.object, recipients)
        return HttpResponseRedirect(self.get_success_url())


class MyTopics(ListView):
    template_name = "meetings/my_topics.html"

    def get_queryset(self):
        try:
            presenter = Presenter.objects.filter(user=self.request.user)
        except Presenter.DoesNotExist:
            return Topic.objects.none()

        return Topic.objects.filter(presenters__in=presenter)


class RSVP(ProcessFormView, ModelFormMixin, TemplateResponseMixin):
    http_method_names = ["post", "get"]
    success_url = reverse_lazy("home")

    def get_template_names(self):
        if self.request.method == "POST":
            return ["meetings/_rsvp_form_response.html"]
        elif self.request.method == "GET":
            return ["meetings/rsvp_form.html"]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.object = None

        def lookup_meeting():
            if self.request.method == "POST":
                meeting_id = self.request.POST.get("meeting", None)

            if self.request.method == "GET":
                meeting_id = self.request.GET.get("meeting", None)

            if not meeting_id:
                raise Http404("Meeting missing from POST")

            try:
                meeting_id = int(meeting_id)
            except (ValueError, TypeError):
                raise Http404("The meeting must be an integer")

            return get_object_or_404(Meeting, pk=meeting_id)

        self.meeting = lookup_meeting()

        if self.request.user.is_authenticated:
            try:
                self.object = RSVPModel.objects.get(user=self.request.user, meeting=self.meeting)
            except RSVPModel.DoesNotExist:
                pass

        # check to see if registration is closed
        if not self.meeting.can_register():
            messages.error(request, "Registration for this meeting is closed.")
            return redirect(reverse_lazy("home"))

        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        authenticated = self.request.user.is_authenticated
        return RSVPForm if authenticated else RSVPFormWithCaptcha

    def form_valid(self, form):
        # calling super.form_valid(form) also does self.object = form.save()
        response = super().form_valid(form)

        messages.success(self.request, "RSVP Successful.")
        if not self.object.user and self.object.email:
            send_rsvp_email(self.object)

        return response

    def get_initial(self):
        initial = {
            "meeting": self.meeting,
            "response": "Y",
        }
        if self.request.user.is_authenticated:
            user = self.request.user
            data = {
                "user": user,
                "email": getattr(user, "email", None),
                "first_name": getattr(user, "first_name", None),
                "last_name": getattr(user, "last_name", None),
            }
            initial.update(data)
        return initial


class UpdateRSVP(UpdateView):
    model = RSVPModel
    form_class = RSVPForm
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.meeting.can_register():
            messages.error(
                self.request, "Registration for this meeting on is closed.",
            )
            return HttpResponseRedirect(reverse_lazy("home"))
        return self.render_to_response(self.get_context_data())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs

    def form_valid(self, form):
        if self.request.method == "POST":
            messages.success(self.request, "RSVP updated succesfully.")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        obj = get_object_or_404(RSVPModel, key=self.kwargs["rsvp_key"])
        return obj

    def get_template_names(self):
        if self.request.method == "POST":
            return ["meetings/_rsvp_form_response.html"]
        elif self.request.method == "GET":
            return ["meetings/rsvp_form.html"]


class RSVPlist(ListView):
    context_object_name = "attendees"
    template_name = "meetings/rsvp_list.html"

    def get_queryset(self):
        self.meeting = get_object_or_404(Meeting, key=self.kwargs["meeting_key"])
        return (
            RSVPModel.objects.filter(meeting=self.meeting)
            .exclude(response="N")
            .order_by("last_name", "first_name")
        )

    def get_context_data(self, **kwargs):  # pylint: disable=arguments-differ
        rsvp_yes = RSVPModel.objects.filter(meeting=self.meeting).exclude(response="N").count()
        context = {"meeting": self.meeting, "guests": (rsvp_yes)}
        context.update(super(RSVPlist, self).get_context_data(**kwargs))
        return context


class RSVPlistCSVBase(RSVPlist):
    def _lookup_rsvps(self, rsvp):
        if self.private:
            yield [
                "User Id",
                "Username",
                "Last Name",
                "First Name",
                "Email",
            ]
        else:
            yield [
                "Last Name",
                "First Name",
            ]

        for item in rsvp:
            if self.private:
                row = [
                    item.user.id if item.user else "",
                    item.user.username if item.user else "",
                    item.last_name,
                    item.first_name,
                    item.email,
                ]
            else:
                row = [
                    item.last_name,
                    item.first_name,
                ]

            yield row

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type="text/csv")
        file_name = slugify(f"chipy-export-{self.meeting.id}--{self.meeting.when}")
        response["Content-Disposition"] = f'attachment; filename="{file_name}.csv"'

        writer = csv.writer(response, quoting=csv.QUOTE_ALL)
        for row in self._lookup_rsvps(context["attendees"]):
            writer.writerow(row)

        return response


class RSVPlistPrivate(RSVPlistCSVBase):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):  # pylint: disable=arguments-differ
        return super(RSVPlistPrivate, self).dispatch(*args, **kwargs)

    private = True


class RSVPlistHost(RSVPlistCSVBase):
    private = False


class PastTopics(ListView):
    context_object_name = "topics"
    template_name = "meetings/past_topics.html"
    queryset = Topic.objects.filter(
        meeting__when__lt=datetime.date.today(), approved=True
    ).order_by("-meeting__when")


class PastTopic(DetailView):
    model = Topic
    template_name = "meetings/past_topic.html"
    context_object_name = "topic"
    pk_url_kwarg = "id"


class MeetingListAPIView(ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingMeetupSync(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meetup_meeting_sync(settings.MEETUP_API_KEY, meeting.meetup_id)
        return Response()


class UpcomingEvents(TemplateView):
    template_name = "meetings/upcoming_events.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        upcoming_events = Meeting.objects.filter(
            when__gt=datetime.datetime.now() - datetime.timedelta(hours=3)
        ).order_by("when")[:5]

        if upcoming_events.count() > 1:
            past_events = Meeting.objects.filter(
                when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
            ).order_by("-when")[:1]
        else:
            past_events = Meeting.objects.filter(
                when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
            ).order_by("when")[:2]

        events = []

        node_orientation = "left"
        for past_event in past_events:
            events.append(
                {
                    "meeting": past_event,
                    "time_status": "inactive",
                    "node_orientation": node_orientation,
                }
            )
            if node_orientation == "left":
                node_orientation = "right"
            else:
                node_orientation = "left"

        for upcoming_event in upcoming_events:
            events.append(
                {
                    "meeting": upcoming_event,
                    "time_status": "active",
                    "node_orientation": node_orientation,
                }
            )
            if node_orientation == "left":
                node_orientation = "right"
            else:
                node_orientation = "left"

        data["events"] = events
        return data
