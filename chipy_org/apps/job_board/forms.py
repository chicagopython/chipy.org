from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea
from chipy_org.apps.sponsors.models import Sponsor
from chipy_org.apps.profiles.models import UserProfile
from .models import JobPost

class JobPostForm(forms.ModelForm):

    class Meta:
        model = JobPost
        
        fields = [
            'company_name',
            'position',
            'description',
            'is_sponsor',
            'company_sponsor',
            'can_host_meeting',
            'link_to_company_page'
        ]
        
        widgets = {
            'description': Textarea(attrs={'cols':80, 'rows':20}),
        }


class JobUserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email'
        ]

      
class JobProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
               'is_external_recruiter'
        ]