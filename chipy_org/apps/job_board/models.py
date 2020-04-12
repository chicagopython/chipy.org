from django.db import models
from datetime import datetime
from chipy_org.libs.models import CommonModel
from chipy_org.apps.sponsors.models import Sponsor
from django.contrib.auth.models import User

MAX_LENGTH = 255

STATUS_CHOICES = [('pending', 'Pending Approval'),
                   ('approved', 'Approved'),
                   ('denied', 'Denied'),
                   ('extended', 'Extended'),
                   ('archived', 'Archived') 
                 ]


class JobPost(CommonModel):
    
    __original_status = None

    company_name = models.CharField(max_length=MAX_LENGTH)
    
    position = models.CharField(max_length=MAX_LENGTH)
    
    description = models.CharField(max_length=2500, help_text = '2500 Character Limit')

    is_sponsor = models.BooleanField(
        default=False, verbose_name="Is the company a sponsor of ChiPy?")

    company_sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

    # After checking to see that the company_name and company_sponsor match, it is then considered verified
    is_verified_sponsor = models.BooleanField(editable=False, default=False)

    can_host_meeting = models.BooleanField(
        default=False, verbose_name="Is your organization interested in hosting an event?")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default='pending')
    
    # - 'status_change_date' is used to calculate relative time, i.e. 3 Days from when Job was first approved for posting
    # - Will also be useful for calculating when post should expire 
    # - This field will change every time you update the 'status' field. Code for doing that is in the 'save' method.
    status_change_date = models.DateTimeField(editable=False, auto_now_add=True) 

    link_to_company_page = models.CharField(max_length=MAX_LENGTH)

    contact = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    def __init__(self, *args, **kwargs):
        super(JobPost, self).__init__(*args, **kwargs)
        self.__original_status = self. status

    def save(self, *args, **kwargs):
        # Every time a decision is made for the status of the post, 
        # the date that the decision is made is updated. 
        
        if  self.__original_status != self.status:
            self.status_change_date = datetime.now()
            self.__original_status = self. status
 
        # The property 'verify_sponsor' is saved in a model field because
        # properties can not be used in filtering querysets.
        # Query filtering and ordering in Django views are based only on fields, not properties.
        self.is_verified_sponsor = self.verify_sponsor

        return super(JobPost, self).save(*args, **kwargs)

    @property
    def days_elapsed(self):

        # computes days elapsed from when job post is put in 'approved' or 'extended' status
        if self.status == 'approved' or self.status == 'extended':
            current_datetime = datetime.now()
            delta = current_datetime - self.status_change_date
            days_elapsed_from_posting = delta.days
            return days_elapsed_from_posting
        else:
            return None
    
    @property
    def verify_sponsor(self):
        # checks to see if the company_name that the user has entered is one of the sponsors
        
        if self.is_sponsor and self.company_sponsor:
            company_name = self.company_name.strip().lower()
            company_sponsor = self.company_sponsor.name.strip().lower()
            return company_name == company_sponsor 
        else:
            return False