import datetime
import csv
import logging

from django.db.models import Sum
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify

from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, ProcessFormView, ModelFormMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
import probablepeople

from chipy_org.apps.meetings.forms import RSVPForm, AnonymousRSVPForm
from .utils import meetup_meeting_sync, unicode_convert
from .email import send_rsvp_email, send_meeting_topic_submitted_email

from .forms import TopicForm, RSVPForm, AnonymousRSVPForm
from .models import (
    Meeting,
    Topic,
    Presentor,
)

from .models import RSVP as RSVPModel
from .serializers import MeetingSerializer

logger = logging.getLogger(__name__)


class PastMeetings(ListView):
    template_name = 'meetings/past_meetings.html'
    queryset = Meeting.objects.filter(
        when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
    ).order_by("-when")


class MeetingDetail(DetailView):
    template_name = 'meetings/meeting.html'
    pk_url_kwarg = 'pk'
    model = Meeting

    def get_context_data(self, **kwargs):
        context = super(MeetingDetail, self).get_context_data(**kwargs)
        context.update(kwargs)
        if self.request.user.is_authenticated():
            context['rsvp_form'] = RSVPForm(self.request)
        else:
            context['rsvp_form'] = AnonymousRSVPForm(self.request)
        return context


class ProposeTopic(CreateView):
    template_name = 'meetings/propose_topic.html'
    form_class = TopicForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super(ProposeTopic, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Topic has been submitted.')
        send_meeting_topic_submitted_email(self.object)
        return HttpResponseRedirect(self.get_success_url())


class MyTopics(ListView):
    template_name = 'meetings/my_topics.html'

    def get_queryset(self):
        try:
            presenter = Presentor.objects.filter(user=self.request.user)
        except Presentor.DoesNotExist:
            return Topic.objects.none()

        return Topic.objects.filter(presentors=presenter)


class RSVP(ProcessFormView, ModelFormMixin, TemplateResponseMixin):
    http_method_names = ['post', 'get']
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):

        self.object = None

        def lookup_meeting():
            meeting_id = self.request.POST.get('meeting', None)
            if not meeting_id:
                raise Http404('Meeting missing from POST')

            try:
                meeting_id = int(meeting_id)
            except (ValueError, TypeError):
                raise Http404("The meeting must be an integer")

            return get_object_or_404(Meeting, pk=meeting_id)

        if self.request.user.is_authenticated() and 'rsvp_key' not in self.kwargs:
            # If the user is logged in
            self.meeting = lookup_meeting()
            try:
                # check to see if they already have registered
                self.object = RSVPModel.objects.get(
                    user=self.request.user, meeting=self.meeting)
            except RSVPModel.DoesNotExist:
                pass
        elif self.request.user.is_anonymous() and 'rsvp_key' not in self.kwargs:
            # If the user is anonymous
            self.meeting = lookup_meeting()
        elif 'rsvp_key' in self.kwargs:
            # If the user has a registration link (typically emailed to them)
            # This is to allow the user to possibly change their response.
            self.object = get_object_or_404(RSVPModel, key=self.kwargs['rsvp_key'])
            self.meeting = self.object.meeting
        else:
            raise Exception("should not get here")

        # check to see if registration is closed
        if not self.meeting.can_register():
            messages.error(request, 'Registration for this meeting is closed.')
            return redirect(reverse_lazy("home"))

        return super(RSVP, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return RSVPForm
        else:
            return AnonymousRSVPForm

    def get_template_names(self):
        if self.request.method == 'POST':
            return ['meetings/_rsvp_form_response.html']
        elif self.request.method == 'GET':
            return ['meetings/rsvp_form.html']

    def get_form_kwargs(self):
        kwargs = {}
        kwargs.update(super(RSVP, self).get_form_kwargs())
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            response = self.form_valid(form)
            messages.success(request, 'RSVP Successful.')

            if not self.object.user and self.object.email:
                send_rsvp_email(self.object)

            return response
        else:
            return self.form_invalid(form)


class RSVPlist(ListView):
    context_object_name = 'attendees'
    template_name = 'meetings/rsvp_list.html'

    def get_queryset(self):
        self.meeting = get_object_or_404(Meeting, key=self.kwargs['meeting_key'])
        return RSVPModel.objects.filter(
            meeting=self.meeting).exclude(response='N').order_by('name')

    def get_context_data(self, **kwargs):
        rsvp_yes = RSVPModel.objects.filter(
            meeting=self.meeting).exclude(response='N').count()
        rsvp_guest = RSVPModel.objects.filter(
            meeting=self.meeting).exclude(
                response='N').aggregate(Sum('guests'))['guests__sum']
        if not rsvp_guest:
            rsvp_guest = 0
        context = {
            'meeting': self.meeting,
            'guests': (rsvp_yes + rsvp_guest)
        }
        context.update(super(RSVPlist, self).get_context_data(**kwargs))
        return context


class RSVPlistCSVBase(RSVPlist):

    def _lookup_rsvps(self, rsvp):
        if self.private:
            yield ["User Id", "Username", "Full Name", "First Name", "Last Name", "Email", "Guests",]
        else:
            yield ["Full Name", "First Name", "Last Name", "Guests",]
        for item in rsvp:
            first_name = last_name = full_name = ""
            if not item.name:
                # if no name is defined and there is a db record for this user
                if item.user:
                    # lookup the user's name from the db
                    first_name = item.user.first_name
                    last_name = item.user.last_name
                    try:
                        full_name = item.user.profile.display_name
                    except Exception as e:
                        logger.exception("Unable to access user profile.")
            else:
                full_name = item.name
                try:
                    # try to parse out the user first/last name
                    parsed = probablepeople.tag(full_name)
                    first_name = parsed[0].get("GivenName")
                    last_name = parsed[0].get("Surname")
                except Exception as e:
                    logger.exception("unable to parse person {}".format(full_name))
            if self.private:
                row = [item.user.id if item.user else "", 
                    item.user.username if item.user else "",
                    full_name,
                    first_name,
                    last_name,
                    item.email,
                    item.guests]
            else:
                row = [
                    full_name,
                    first_name,
                    last_name,
                    item.guests]
            row = [unicode_convert(x) for x in row]
            yield row

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(content_type='text/csv')
        file_name = slugify("chipy-export-{id}--{date}".format(
            id=self.meeting.id, date=self.meeting.when))
        response['Content-Disposition'] = 'attachment; filename="%s.csv"' % file_name

        writer = csv.writer(response, quoting=csv.QUOTE_ALL)
        for row in self._lookup_rsvps(context['attendees']):
            writer.writerow(row)

        return response


class RSVPlistPrivate(RSVPlistCSVBase):

    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(RSVPlistPrivate, self).dispatch(*args, **kwargs)

    private = True
 

class RSVPlistHost(RSVPlistCSVBase):
    private = False


class PastTopics(ListView):
    context_object_name = 'topics'
    template_name = 'meetings/past_topics.html'
    queryset = Topic.objects.filter(
        meeting__when__lt=datetime.date.today(), approved=True).order_by("-meeting__when")


class PastTopic(DetailView):
    model = Topic
    template_name = "meetings/past_topic.html"
    context_object_name = "topic"
    pk_url_kwarg = 'id'


class MeetingListAPIView(ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingMeetupSync(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meetup_meeting_sync(settings.MEETUP_API_KEY, meeting.meetup_id)
        return Response()
