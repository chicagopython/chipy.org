from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import UserProfile
from .forms import ProfileForm

class ProfilesList(ListView):
    context_object_name = 'profiles'
    template_name = 'profiles/list.html'
    queryset = User.objects.filter(profile__show = True)

class ProfileEdit(UpdateView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = '/'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user = self.request.user)
