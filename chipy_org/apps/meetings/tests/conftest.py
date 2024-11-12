import pytest
from django.conf import global_settings
from django.test import override_settings

@pytest.fixture(autouse=True)
def with_static_files():
    with override_settings(STORAGES=global_settings.STORAGES):
        yield
