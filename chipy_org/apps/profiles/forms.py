from django.forms import ModelForm
from profiles.models import UserProfile

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

