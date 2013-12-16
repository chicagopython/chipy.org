import datetime
from django.views.generic import TemplateView
from apps.meetings.models import Meeting, RSVP
from apps.meetings.forms import RSVPForm


class Home(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)

        future_meetings = Meeting.objects.filter(when__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

        if future_meetings.count() == 0:
            context['next_meeting'] = False
        else:
            next_meeting = future_meetings.order_by('when')[0]
            next_meeting.topics_list = list()
            for topic in next_meeting.topics.filter(approved=True).order_by('start_time'):
                topic.minutes = topic.length.seconds / 60
                next_meeting.topics_list.append(topic)

            context['next_meeting'] = next_meeting

            # Check if user and get rsvp
            if self.request.user.is_authenticated():
                # Is there already an RSVP
                if RSVP.objects.filter(meeting=next_meeting, user=self.request.user).exists():
                    context['rsvp'] = RSVP.objects.get(meeting=next_meeting, user=self.request.user)
                else:
                    context['rsvp'] = None

            context['rsvp_form'] = RSVPForm(self.request)

        return context
