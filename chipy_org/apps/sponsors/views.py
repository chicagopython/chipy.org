import datetime
from datetime import date

from django.views.generic import DetailView, ListView
from .models import Sponsor, SponsorGroup
from ..meetings.models import Meeting


class SponsorDetailView(DetailView):
    model = Sponsor
    context_object_name = "sponsor"
    template_name = "sponsors/sponsor_detail.html"


class SponsorListView(ListView):
    model = SponsorGroup
    context_object_name = "sponsor_groups"
    template_name = "sponsors/sponsor_list.html"

    def get_queryset(self):
        return (
            super(SponsorListView, self)
            .get_queryset()
            .filter(sponsors__isnull=False)
            .prefetch_related("sponsors")
            .order_by("list_priority", "name")
            .distinct()
        )

    def get_context_data(self, **kwargs): # pylint: disable=arguments-differ

        meeting_queryset = Meeting.objects.all().filter(
            when__range=((date.today() - datetime.timedelta(days=365), date.today()))
        )
        meeting_attendees = 0
        for meeting in meeting_queryset:
            meeting_attendees = meeting_attendees + int(meeting.number_rsvps())

        sponsor_groups = (
            super(SponsorListView, self)
            .get_queryset()
            .filter(sponsors__isnull=False)
            .prefetch_related("sponsors")
            .order_by("list_priority", "name")
            .distinct()
        )

        context = {
            "meeting_attendees": meeting_attendees,
            "sponsor_groups": sponsor_groups,
        }

        return context
