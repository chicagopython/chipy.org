import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Now

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


class ApprovedAndActive(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(status="AP") & Q(approval_date__gte=Now() - F("time_to_expire")))
        )


class Affiliation(CommonModel):
    description = models.CharField(max_length=MAX_LENGTH)
    url = models.URLField()

    def __str__(self):
        return self.description


class JobPost(CommonModel):

    __original_status = None

    company_name = models.CharField(max_length=MAX_LENGTH)

    position = models.CharField(max_length=MAX_LENGTH)

    description = models.CharField(
        max_length=5000,
        help_text="5000 Character Limit. Create a new paragraph by pressing 'Enter' twice.",
    )

    is_sponsor = models.BooleanField(
        default=False, verbose_name="Is the company a sponsor of ChiPy?"
    )

    affiliation = models.ForeignKey(
        Affiliation, blank=True, null=True, on_delete=models.DO_NOTHING,
    )

    can_host_meeting = models.BooleanField(
        default=False, verbose_name="Is your organization interested in hosting an event?"
    )

    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="SU")

    approval_date = models.DateTimeField(editable=False, blank=True, null=True)

    time_to_expire = models.DurationField(
        default=datetime.timedelta(days=NUM_DAYS_T0_EXPIRE),
        verbose_name="Num of days for post to show",
    )

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

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ

        if self.status == "AP":
            # If post is approved and the approval_date hasn't been set yet,
            # set the approval_date.
            if not self.approval_date:
                self.approval_date = datetime.datetime.now()

        # If post was approved but then changed to a different status,
        # set the approval_date back to None.
        elif self.approval_date:
            self.approval_date = None

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

    def approve(self):
        self.status = "AP"
        self.save()

    @property
    def expiration_date(self):

        # expiration_date shows up as a field in the admin panel.
        # If post is approved and the approval_date is set,
        # compute the expiration_date.
        if self.status == "AP" and self.approval_date:
            expiration_date = self.approval_date + self.time_to_expire
            return expiration_date
        else:
            return None

    objects = models.Manager()
    approved_and_active = ApprovedAndActive()
