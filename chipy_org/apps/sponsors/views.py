from django.shortcuts import render
from .models import Sponsor
from django.views.generic import DetailView


class SponsorDetailView(DetailView):
    model = Sponsor
    context_object_name = "sponsor"
    template_name = "sponsors/sponsor_detail.html"
