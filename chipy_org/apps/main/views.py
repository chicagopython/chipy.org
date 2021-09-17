import datetime
import sys
import traceback

from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader
from django.views.generic import TemplateView

from chipy_org.apps.meetings.models import Meeting
from chipy_org.apps.meetings.views import InitialRSVPMixin
from chipy_org.apps.sponsors.models import Sponsor


class Home(TemplateView, InitialRSVPMixin):
    template_name = "main/homepage.html"
    message_as_modal = True

    def get_meeting(self):
        return (
            Meeting.objects.filter(when__gt=datetime.datetime.now() - datetime.timedelta(hours=6))
            .order_by("when")
            .first()
        )

    def get_context_data(self, **kwargs):
        context = {}
        context.update(kwargs)
        context["IS_HOMEPAGE"] = True
        context["featured_sponsor"] = Sponsor.featured_sponsor()
        context["message_as_modal"] = self.message_as_modal

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


def custom_404(request, exception):
    return HttpResponse("<h1>404 - Page Not Found</h1>", status=404)


class LogoutWithRedirectAndMessage(LogoutView):
    next_page = "/"

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You've been logged out")
        return super().dispatch(request, *args, **kwargs)
