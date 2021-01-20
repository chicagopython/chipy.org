import pytest
from django.conf.global_settings import DEBUG
from django.core.management import call_command
from django.test import override_settings

pytestmark = pytest.mark.django_db


@override_settings(DEBUG=True)
def test_make_dev_data():
    call_command("makedevdata")
