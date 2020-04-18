import datetime

import sys
import traceback

from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.views.generic import TemplateView
from chipy_org.apps.meetings.models import Meeting
from chipy_org.apps.meetings.views import InitialRSVPMixin
from chipy_org.apps.sponsors.models import GeneralSponsor
from chipy_org.apps.announcements.models import Announcement


class Home(TemplateView, InitialRSVPMixin):
    template_name = "homepage.html"

    def get_non_main_meetings(self, num):
        return (
            Meeting.objects.filter(meeting_type__isnull=False)
            .filter(when__gt=datetime.datetime.now() - datetime.timedelta(hours=6))
            .order_by("when")[:num]
        )

    def get_meeting(self):
        return (
            Meeting.objects.filter(meeting_type__isnull=True)
            .filter(when__gt=datetime.datetime.now() - datetime.timedelta(hours=6))
            .order_by("when")
            .first()
        )

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)
        context["other_meetings"] = self.get_non_main_meetings(num=3)
        context["general_sponsors"] = GeneralSponsor.objects.all().order_by("?")
        context["announcement"] = Announcement.objects.featured()
        context = self.add_extra_context(context)
        return context


def custom_500(request):
    template = loader.get_template("500.html")

    print(sys.exc_info())
    etype, value, tback = sys.exc_info()
    return HttpResponseServerError(
        template.render(
            {
                "exception_value": value,
                "value": etype,
                "tb": traceback.format_exception(etype, value, tback),
            }
        )
    )


def customer_404(request, e):
    return HttpResponse('<h1>404 - Page Not Found</h1>', status=404)
