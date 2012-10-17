import datetime
from django.views.generic import TemplateView
from meetings.models import Meeting

class Home(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)

        future_meetings = Meeting.objects.filter(when__gt = datetime.datetime.now() - datetime.timedelta(hours = 3))

        if future_meetings.count() == 0:
            context['next_meeting'] = False
        else:
            next_meeting = future_meetings.order_by('-when')[0]
            next_meeting.topics = list()
            for topic in next_meeting.topic_set.filter(approved = True):
                topic.minutes = topic.length.seconds / 60
                next_meeting.topics.append(topic)

            context['next_meeting'] = next_meeting
            
        return context


