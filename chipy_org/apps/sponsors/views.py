from django.views.generic import DetailView, ListView
from .models import Sponsor, SponsorGroup


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
            .prefetch_related('sponsors')
            .order_by('list_priority', 'name')
            .distinct()
        )
