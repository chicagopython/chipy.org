from django.views.generic import ListView
from django.contrib.auth.models import User

class ProfilesList(ListView):
    model = User
    context_object_name = 'profiles'
    template_name = 'profiles/list.html'
