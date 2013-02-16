import datetime

from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, ProcessFormView, ModelFormMixin
from django.contrib import messages

from meetings.models import (Meeting,
                             Topic,
                             Presentor)

from meetings.models import RSVP as RSVPModel

from meetings.forms import TopicForm, RSVPForm

class PastMeetings(ListView):
    template_name = 'meetings/past_meetings.html'
    queryset = Meeting.objects.filter(when__lt = datetime.datetime.now() - datetime.timedelta(hours = 3))

class ProposeTopic(CreateView):
    template_name = 'meetings/propose_topic.html'
    form_class = TopicForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(ProposeTopic, self).get_form_kwargs()
        kwargs.update({'request':self.request})
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
            presentor = Presentor.objects.filter(user = self.request.user)
        except Presentor.DoesNotExist:
            return Topic.objects.none()

        return Topic.objects.filter(presentor = presentor)


class RSVP(ProcessFormView, ModelFormMixin, TemplateResponseMixin):
    http_method_names = ['post', 'get']
    form_class = RSVPForm
    success_url = '/'

    def get_template_names(self):
        if self.request.method == 'POST':
            return ['meetings/_rsvp_form_response.html']
        elif  self.request.method == 'GET':
            return ['meetings/rsvp_form.html']

    def get_form_kwargs(self):
        kwargs = {}
        if not kwargs.get('instance', False) and self.request.user.is_authenticated() and 'rsvp_key' not in self.kwargs:
            try:
                meeting = Meeting.objects.get(pk = self.request.POST['meeting'])
                self.object = RSVPModel.objects.get(user = self.request.user, meeting = meeting)
            except RSVPModel.DoesNotExist:
                pass
        elif not self.request.user.is_authenticated():
            # Try and pull it from its key
            if 'rsvp_key' in self.kwargs:
                self.object = RSVPModel.objects.get(key = self.kwargs['rsvp_key'])

        kwargs.update(super(RSVP, self).get_form_kwargs())
        kwargs.update({'request':self.request})

        return kwargs

    def get_form(self, form_class):
        form = super(RSVP, self).get_form(form_class)
        if 'rsvp_key' in self.kwargs:
            del form.fields['meeting']
        return form

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            # Set message
            messages.success(request, 'RSVP Successful.')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PastTopics(ListView):
    context_object_name = 'topics'
    template_name = 'meetings/past_topics.html'
    queryset = Topic.objects.filter(meeting__when__lt = datetime.date.today(), approved = True)
