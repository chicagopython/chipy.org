from django.db import models
from django.utils import timezone
from chipy_org.libs.models import CommonModel
from chipy_org.apps.sponsors.models import Sponsor

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
    
    description = models.CharField(max_length=2500)

    is_sponsor = models.BooleanField(
        default=False, verbose_name="Is the company a sponsor of ChiPy?")

    company_sponsor = models.ForeignKey(Sponsor, blank=True, null=True)

    can_host_meeting = models.BooleanField(
        default=False, verbose_name="Is your organization interested in hosting an event?")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default='pending')
    
    # - 'status_change_date' is used to calculate relative time, i.e. 3 Days from when Job was first approved for posting
    # - Will also be useful for calculating when post should expire 
    # - This field will change every time you update the 'status' field. Code for doing that is in the 'save' method.
    status_change_date = models.DateTimeField(editable=False, auto_now_add=True) 

    link_to_company_page = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    def __init__(self, *args, **kwargs):
        super(JobPost, self).__init__(*args, **kwargs)
        self.__original_status = self. status

    def save(self, *args, **kwargs):
        ''' Every time a decision is made for the status of the post, 
        the date that the decision is made is updated. '''
        
        if  self.__original_status != self.status:
            self.status_change_date = timezone.now()
            self.__original_status = self. status

        return super(JobPost, self).save(*args, **kwargs)