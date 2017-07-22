from .models import Sponsor
from django.views.generic import DetailView, ListView


class SponsorDetailView(DetailView):
    model = Sponsor
    context_object_name = "sponsor"
    template_name = "sponsors/sponsor_detail.html"


class SponsorListView(ListView):
    model = Sponsor
    context_object_name = "sponsors"
    template_name = "sponsors/sponsor_list.html"

    def get_queryset(self):
        return super(SponsorListView, self).get_queryset().order_by('name')
