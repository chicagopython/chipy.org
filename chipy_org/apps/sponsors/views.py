import datetime
from datetime import date

from django.views.generic import DetailView, ListView
<<<<<<< HEAD
from .models import Sponsor, SponsorGroup

=======
from .models import Sponsor
from ..meetings.models import Meeting
>>>>>>> commited to

class SponsorDetailView(DetailView):
    model = Sponsor
    context_object_name = "sponsor"
    template_name = "sponsors/sponsor_detail.html"


class SponsorListView(ListView):
<<<<<<< HEAD
    model = SponsorGroup
    context_object_name = "sponsor_groups"
    template_name = "sponsors/sponsor_list.html"

    def get_queryset(self):
        return (
            super(SponsorListView, self)
                .get_queryset()
                .filter(sponsors__isnull=False)
                .prefetch_related('sponsors')
                .order_by('list_priority', 'name')
                .distinct()
        )
=======
	context_object_name = "sponsors"
	template_name = "sponsors/sponsor_list.html"
   	queryset = Sponsor.objects.all()

	def get_context_data(self, *args, **kwargs):
		sponsor_list = Sponsor.objects.all().order_by('name')
		meeting_queryset = Meeting.objects.all().filter(when__range=((date.today() - datetime.timedelta(days=365),date.today())))
		meeting_attendees = 0
		for meeting in meeting_queryset:
			meeting_attendees = meeting_attendees + int(meeting.number_rsvps())

		context = {
	    	'sponsors' : sponsor_list,
	    	'meeting_attendees' : meeting_attendees,
	    }

		return context
>>>>>>> commited to
