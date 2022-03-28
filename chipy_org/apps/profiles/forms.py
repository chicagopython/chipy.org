from django.forms import ModelForm

from .models import UserProfile


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "display_name",
            "public_email",
            "public_website",
            "bio",
            "show",
        ]
