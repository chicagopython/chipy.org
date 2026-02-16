from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, UpdateView

from .forms import ProfileForm
from .models import CustomFlatPage, UserProfile


def custom_flatpage_view(request, url):
    flatpage = get_object_or_404(CustomFlatPage, url=url)
    return render(request, "shiny/slim.html", {"flatpage": flatpage})


class ProfilesList(ListView):
    context_object_name = "profiles"
    template_name = "profiles/list.html"
    queryset = User.objects.filter(profile__show=True)


class ProfilesListOrganizers(ListView):
    context_object_name = "organizers"
    template_name = "profiles/organizers.html"
    queryset = UserProfile.user_organizers()
    ordering = ["profile__display_name"]


class ProfileEdit(UpdateView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = "/"

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
