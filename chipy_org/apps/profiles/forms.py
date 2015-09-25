from django.forms import ModelForm
from .models import UserProfile

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
