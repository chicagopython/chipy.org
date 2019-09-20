import datetime
from datetime import date

from django.views.generic import DetailView, ListView
from .models import Sponsor
from ..meetings.models import Meeting

class SponsorDetailView(DetailView):
    model = Sponsor
    context_object_name = "sponsor"
    template_name = "sponsors/sponsor_detail.html"


class SponsorListView(ListView):
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