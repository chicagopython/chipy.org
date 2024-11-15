import datetime

import pytest
from django.conf import global_settings
from django.test import override_settings

from ..models import JobPost


@pytest.fixture
def job_post():
    # create a job posting
    post = JobPost(
        company_name="test-company",
        position="test-position",
        description="test-description",
        is_sponsor=False,
        can_host_meeting=False,
        status="SU",
        time_to_expire=datetime.timedelta(days=10),
        company_website="www.example.com",
        agree_to_terms=True,
        is_from_recruiting_agency=False,
    )
    post.save()
    return post


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):  # pylint: disable=invalid-name
    pass


@pytest.fixture(autouse=True)
def with_static_files():
    with override_settings(STORAGES=global_settings.STORAGES):
        yield
