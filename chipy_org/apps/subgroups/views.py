from django.shortcuts import render
from django.views.generic import DetailView
from .models import SubGroup


class GroupDetail(DetailView):
    template_name = 'meetings/group.html'
    model = SubGroup
    context_object_name = "group"
