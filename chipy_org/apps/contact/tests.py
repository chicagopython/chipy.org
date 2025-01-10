from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.core import mail
from django_recaptcha.client import RecaptchaResponse

from .forms import ContactForm


@pytest.fixture
def user():
    return User.objects.get_or_create(username="test_user")[0]


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def mocked_captcha():
    mocked_submit = patch("django_recaptcha.fields.client.submit")
    mocked_submit.return_value = RecaptchaResponse(is_valid=True)
    yield


@pytest.mark.django_db
def test_chipy_contact_form(mocked_captcha):  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0

    form_data = {
        "email": "test@test.com",
        "g-recaptcha-response": "PASSED",
        "message": "test message",
        "sender": "test",
        "subject": "test subject",
    }

    form = ContactForm(form_data)

    assert form.is_valid()
    form.send_email()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_chipy_contact_view(authenticated_client):  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0
    response = authenticated_client.post(
        "/contact/",
        {
            "email": "test@test.com",
            "g-recaptcha-response": "PASSED",
            "message": "test message",
            "sender": "test",
            "subject": "test subject",
        },
        follow=True,
    )
    assert response.status_code == 200

    assert b"Your message has been sent to" in response.content
    assert len(mail.outbox) == 1
