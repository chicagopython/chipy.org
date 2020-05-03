from django.contrib.auth.models import User
from django.db import models

from chipy_org.libs.models import CommonModel


class SubGroup(CommonModel):

    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to="group_images", blank=True, null=True,)
    slug = models.SlugField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=True)
    organizers = models.ManyToManyField(User, blank=True)

    def __unicode__(self):
        return f"{self.id} | ({self.name})"

    class Meta:
        verbose_name = "Sub Group (SIG)"
        verbose_name_plural = "Sub Groups (SIGs)"
