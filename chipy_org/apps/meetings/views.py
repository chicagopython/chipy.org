import datetime

from django.db.models import Sum
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import get_object_or_404

from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, ProcessFormView, ModelFormMixin
from django.contrib import messages

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from chipy_org.apps.meetings.utils import meetup_meeting_sync



from .forms import TopicForm, RSVPForm
from .models import (
    Meeting,
    Topic,
    Presentor
)
from .models import RSVP as RSVPModel
from .serializers import MeetingSerializer


class PastMeetings(ListView):
    template_name = 'meetings/past_meetings.html'
    queryset = Meeting.objects.filter(
        when__lt=datetime.datetime.now() - datetime.timedelta(hours=3)
    ).order_by("-when")


class ProposeTopic(CreateView):
    template_name = 'meetings/propose_topic.html'
    form_class = TopicForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(ProposeTopic, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            # Set message
            messages.success(request, 'Topic has been submitted.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class MyTopics(ListView):
    template_name = 'meetings/my_topics.html'

    def get_queryset(self):
        try:
            presentor = Presentor.objects.filter(user=self.request.user)
        except Presentor.DoesNotExist:
            return Topic.objects.none()

        return Topic.objects.filter(presentors=presentor)


class RSVP(ProcessFormView, ModelFormMixin, TemplateResponseMixin):
    http_method_names = ['post', 'get']
    form_class = RSVPForm
    success_url = '/'

    def get_template_names(self):
        if self.request.method == 'POST':
            return ['meetings/_rsvp_form_response.html']
        elif self.request.method == 'GET':
            return ['meetings/rsvp_form.html']

    def get_form_kwargs(self):
        kwargs = {}
        self.object = None
        if not kwargs.get('instance', False) and self.request.user.is_authenticated() and 'rsvp_key' not in self.kwargs:
            if not self.request.POST.get('meeting'):
                raise ValidationError('Meeting missing from POST')

            try:
                meeting = Meeting.objects.get(pk=self.request.POST['meeting'])
                self.object = RSVPModel.objects.get(user=self.request.user, meeting=meeting)
            except RSVPModel.DoesNotExist:
                pass
        elif 'rsvp_key' in self.kwargs:
            self.object = RSVPModel.objects.get(key=self.kwargs['rsvp_key'])

        kwargs.update(super(RSVP, self).get_form_kwargs())
        kwargs.update({'request': self.request})

        return kwargs

    def get_form(self, form_class):
        form = super(RSVP, self).get_form(form_class)
        if 'rsvp_key' in self.kwargs:
            del form.fields['meeting']
        return form

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            response = self.form_valid(form)
            messages.success(request, 'RSVP Successful.')

            if not self.object.user and self.object.email:
                plaintext = get_template('meetings/rsvp_email.txt')
                htmly = get_template('meetings/rsvp_email.html')

                d = Context({'key': self.object.key, 'site': Site.objects.get_current()})

                subject = 'Chipy: Link to Change your RSVP'
                from_email = 'DoNotReply@chipy.org'
                text_content = plaintext.render(d)
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, text_content, from_email, [self.object.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            return response
        else:
            return self.form_invalid(form)


class RSVPlist(ListView):
    context_object_name = 'attendees'
    template_name = 'meetings/rsvp_list.html'

    def get_queryset(self):
        self.meeting = Meeting.objects.get(key=self.kwargs['rsvp_key'])
        return RSVPModel.objects.filter(meeting=self.meeting).exclude(response='N').order_by('name')

    def get_context_data(self, **kwargs):
        context = {
            'meeting': self.meeting,
            'guests': (
                RSVPModel.objects.filter(meeting=self.meeting).exclude(response='N').len() +
                RSVPModel.objects.filter(meeting=self.meeting).exclude(response='N').aggregate(Sum('guests'))
            )
        }
        context.update(super(RSVPlist, self).get_context_data(**kwargs))
        return context


class PastTopics(ListView):
    context_object_name = 'topics'
    template_name = 'meetings/past_topics.html'
    queryset = Topic.objects.filter(meeting__when__lt=datetime.date.today(), approved=True)


class MeetingListAPIView(ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer


class MeetingMeetupSync(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, meeting_id):
        meeting = get_object_or_404(Meeting, pk=meeting_id)
        meetup_meeting_sync(settings.MEETUP_API_KEY, meeting.meetup_id)
        return Response()
