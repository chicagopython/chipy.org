import datetime

import sys
import traceback

from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, Context
from django.views.generic import TemplateView
from chipy_org.apps.meetings.models import Meeting, RSVP
from chipy_org.apps.meetings.forms import RSVPForm, AnonymousRSVPForm
from chipy_org.apps.sponsors.models import GeneralSponsor
from chipy_org.apps.announcements.models import Announcement


class Home(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)

        # get upcoming main meeting
        future_meetings = Meeting.objects.filter(
            meeting_type__isnull=True).filter(
                when__gt=datetime.datetime.now() - datetime.timedelta(hours=24))

        # get next 3 non-main meetings
        other_meetings = Meeting.objects.filter(
            meeting_type__isnull=False).filter(
                when__gt=datetime.datetime.now() - datetime.timedelta(hours=24)
            ).order_by('when')[:3]
        context['other_meetings'] = other_meetings

        context["general_sponsors"] = GeneralSponsor.objects.all(
            ).order_by('?')

        if future_meetings.count() == 0:
            context['next_meeting'] = False
        else:
            next_meeting = future_meetings.order_by('when')[0]
            context['next_meeting'] = next_meeting

            # Check if user and get rsvp
            if self.request.user.is_authenticated():
                # Is there already an RSVP
                if RSVP.objects.filter(
                        meeting=next_meeting,
                        user=self.request.user).exists():
                    context['rsvp'] = RSVP.objects.get(
                        meeting=next_meeting,
                        user=self.request.user)
                else:
                    context['rsvp'] = None

                context['rsvp_form'] = RSVPForm(self.request)
            else:
                context['rsvp_form'] = AnonymousRSVPForm(self.request)

        context['announcement'] = Announcement.objects.featured()
        return context


def custom_500(request):
    template = loader.get_template('500.html')

    print(sys.exc_info())
    etype, value, tback = sys.exc_info()
    return HttpResponseServerError(template.render(Context({
        'exception_value': value,
        'value': etype,
        'tb': traceback.format_exception(etype, value, tback)})))


def customer_404(request):
    return HttpResponse('<h1>404 - Page Not Found</h1>', status=404)
