from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic import UpdateView

from profiles.models import UserProfile
from profiles.forms import ProfileForm

class ProfilesList(ListView):
    model = User
    context_object_name = 'profiles'
    template_name = 'profiles/list.html'

class ProfileEdit(UpdateView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = '/'
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get(user = self.request.user)