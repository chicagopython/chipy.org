import datetime
import csv

from django.db.models import Sum
from django.conf import settings
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
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
from .utils import meetup_meeting_sync
from .email import send_rsvp_email, send_meeting_topic_submitted_email

from .forms import TopicForm, RSVPForm, AnonymousRSVPForm
from .models import (
    Meeting,
    Topic,
    Presentor,
)

from .models import RSVP as RSVPModel
from .serializers import MeetingSerializer


class PastMeetings(ListView):
    template_name = 'meetings/past_meetings.html'
    queryset = Meeting.objects.filter(
        when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
    ).order_by("-when")


class MeetingDetail(DetailView):
    template_name = 'meetings/meeting.html'
    pk_url_kwarg = 'pk'
    model = Meeting


class ProposeTopic(CreateView):
    template_name = 'meetings/propose_topic.html'
    form_class = TopicForm
    success_url = '/'

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
    success_url = '/'

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
        self.object = None
        if not kwargs.get('instance', False) and self.request.user.is_authenticated() \
           and 'rsvp_key' not in self.kwargs:
            if not self.request.POST.get('meeting'):
                raise ValidationError('Meeting missing from POST')

            try:
                meeting = get_object_or_404(Meeting, pk=self.request.POST['meeting'])
                self.object = RSVPModel.objects.get(
                    user=self.request.user, meeting=meeting)
            except RSVPModel.DoesNotExist:
                pass
        elif 'rsvp_key' in self.kwargs:
            self.object = get_object_or_404(RSVPModel, key=self.kwargs['rsvp_key'])

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
        self.meeting = get_object_or_404(Meeting, key=self.kwargs['rsvp_key'])
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
                        print("Unable to access user profile.")
            else:
                full_name = item.name
                try:
                    # try to parse out the user first/last name
                    parsed = probablepeople.tag(full_name)
                    first_name = parsed[0].get("GivenName")
                    last_name = parsed[0].get("Surname")
                except Exception as e:
                    print("unable to parse person {}".format(full_name))
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
