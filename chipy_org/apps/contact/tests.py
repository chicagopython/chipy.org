import pytest
from django.core import mail
from .forms import ContactForm


from unittest.mock import patch

from django_recaptcha.client import RecaptchaResponse

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


def test_chipy_contact_view(client):  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0

    response = client.post(
        "/contact/",
        {
            "email": "test@test.com",
            "message": "test message",
            "sender": "test",
            "subject": "test subject",
        },
        follow=True,
    )
    assert response.status_code == 200


#    assert b"Your message has been sent to" in response.content
#    assert len(mail.outbox) == 1
