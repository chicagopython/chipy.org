import datetime

import sys
import traceback

from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, Context
from django.views.generic import TemplateView
from chipy_org.apps.meetings.models import Meeting, RSVP
from chipy_org.apps.meetings.forms import RSVPForm, RSVPFormWithCaptcha
from chipy_org.apps.sponsors.models import GeneralSponsor
from chipy_org.apps.announcements.models import Announcement


class Home(TemplateView):
    template_name = 'homepage.html'

    def get_next_main_meeting(self):
        return (Meeting.objects
            .filter(meeting_type__isnull=True)
            .filter(when__gt=datetime.datetime.now()-datetime.timedelta(hours=6))
            .order_by('when')
            .first()
        )
    
    def get_non_main_meetings(self, num):
        return (Meeting.objects
            .filter(meeting_type__isnull=False)
            .filter(when__gt=datetime.datetime.now()-datetime.timedelta(hours=6))
            .order_by('when')[:num]
        )

    def get_initial(self, next_main_meeting):
        # note: not inherited from TemplateView 
        initial = {'response': 'Y'}
        initial.update({'meeting': next_main_meeting})
        if self.request.user.is_authenticated():
            user = self.request.user
            user_data = {
                'user': user,
                'email': getattr(user, 'email', None),
                'first_name': getattr(user, 'first_name', None),
                'last_name': getattr(user, 'last_name', None),
            }
            initial.update(user_data)
        return initial

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return RSVPForm
        else:
            return RSVPFormWithCaptcha

    def get_form(self, request, **kwargs):
        form_class = self.get_form_class()
        return form_class(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)
        context['other_meetings'] = self.get_non_main_meetings(num=3)
        context["general_sponsors"] = GeneralSponsor.objects.all().order_by('?')
        context['announcement'] = Announcement.objects.featured()
        
        next_main_meeting = self.get_next_main_meeting()
        context['next_meeting'] = next_main_meeting 

        if next_main_meeting: 
            initial = self.get_initial(next_main_meeting)
            context['rsvp_form'] = self.get_form(self.request, initial=initial)

            if self.request.user.is_authenticated():
                try:
                    context['rsvp'] = (RSVP.objects
                        .get(meeting=next_main_meeting, user=self.request.user)
                    )
                except:
                    context['rsvp'] = None

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
