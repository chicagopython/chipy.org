import datetime

from django.contrib.auth.models import User
from django.db import models

from chipy_org.libs.models import CommonModel

MAX_LENGTH = 100
NUM_DAYS_T0_EXPIRE = 60

STATUS_CHOICES = [
    ("SU", "Submitted"),
    ("AP", "Approved"),
    ("RE", "Rejected"),
]

LOCATION_CHOICES = [
    ("CH", "Chicago"),
    ("CT", "Chicago and Temporarily Remote"),
    ("CR", "Chicago and Remote"),
    ("RO", "Remote Only"),
]

JOB_TYPE_CHOICES = [
    ("FT", "Full-Time"),
    ("PT", "Part-Time"),
    ("CO", "Contract to Hire Full-Time"),
    ("PI", "Paid Internship"),
    ("PA", "Paid Apprenticeship"),
]


class JobPost(CommonModel):

    __original_status = None

    company_name = models.CharField(max_length=MAX_LENGTH)

    position = models.CharField(max_length=MAX_LENGTH)

    description = models.CharField(
        max_length=2500,
        help_text="2500 Character Limit. Create a new paragraph by pressing 'Enter' twice.",
    )

    is_sponsor = models.BooleanField(
        default=False, verbose_name="Is the company a sponsor of ChiPy?"
    )

    can_host_meeting = models.BooleanField(
        default=False, verbose_name="Is your organization interested in hosting an event?"
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="SU")

    # This field will change every time you update the 'status'
    # field. Code for doing that is in the 'save' method.
    status_change_date = models.DateTimeField(editable=False, auto_now_add=True)

    approval_date = models.DateTimeField(editable=False, blank=True, null=True)

    days_to_expire = models.IntegerField(
        default=NUM_DAYS_T0_EXPIRE, verbose_name="Num of days for post to show"
    )

    expiration_date = models.DateTimeField(editable=False, blank=True, null=True)

    location = models.CharField(
        max_length=2,
        choices=LOCATION_CHOICES,
        default="CH",
        help_text=(
            "ChiPy is a locally based group."
            " Position must not move candidate out of the Chicago area."
            " Working remote or commuting is acceptable. Any position requiring relocation"
            " out of the Chicagoland area is out of scope of the mission of the group."
        ),
    )

    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES, default="FT")

    company_website = models.CharField(max_length=MAX_LENGTH)

    how_to_apply = models.CharField(
        max_length=2500,
        help_text="2500 Character Limit. Create a new paragraph by pressing 'Enter' twice.",
    )

    contact = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)

    agree_to_terms = models.BooleanField(
        verbose_name="I have read and agree to the referral terms, "
        "which includes giving a referral fee when a candidate is hired/placed."
    )

    is_from_recruiting_agency = models.BooleanField(
        default=False, verbose_name="Is this posting from a recruiting agency?"
    )

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    def __init__(self, *args, **kwargs):
        super(JobPost, self).__init__(*args, **kwargs)
        self.__original_status = self.status
        self.__original_days_to_expire = self.days_to_expire

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        # Every time a decision is made for the status of the post,
        # the date that the decision is made is updated.

        if self.__original_status != self.status:
            self.status_change_date = datetime.datetime.now()
            self.__original_status = self.status

        # If post is approved and the approval_date hasn't been set yet,
        # set the approval_date and expiration_date.
        if self.status == "AP" and not self.approval_date:

            self.approval_date = datetime.datetime.now()
            self.expiration_date = self.approval_date + datetime.timedelta(days=self.days_to_expire)

            # If days_to_expire is being changed from its initial default value,
            # it will differ from the __original_days_to_expire field.
            # If that's the case, change __original_days_to_expire so that in
            # the future, we can keep track of when the days_to_expire field changes.
            if self.__original_days_to_expire != self.days_to_expire:
                self.__original_days_to_expire = self.days_to_expire

        # If post is approved AND expiration_date has been set AND days_to_expire is changed,
        # then recalculate expiration_date.
        elif (
            self.status == "AP"  # pylint: disable=bad-continuation
            and self.approval_date  # pylint: disable=bad-continuation
            and self.__original_days_to_expire  # pylint: disable=bad-continuation
            != self.days_to_expire  # pylint: disable=bad-continuation
        ):

            self.expiration_date = self.approval_date + datetime.timedelta(days=self.days_to_expire)
            self.__original_days_to_expire = self.days_to_expire

        super(JobPost, self).save(*args, **kwargs)

    @property
    def days_elapsed(self):

        # computes days elapsed from when job post is put in 'approved' status
        if self.status == "AP" and self.approval_date:
            current_datetime = datetime.datetime.now()
            delta = current_datetime - self.approval_date
            days_elapsed_from_posting = delta.days
            return days_elapsed_from_posting
        else:
            return None
