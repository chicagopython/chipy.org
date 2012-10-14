import datetime

from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages

from meetings.models import (Meeting,
                             Topic,
                             Presentor)

from meetings.forms import TopicForm

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
