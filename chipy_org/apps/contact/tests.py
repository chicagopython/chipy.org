import pytest
from django.conf import global_settings
from django.core import mail
from django.test import override_settings

from .forms import ContactForm


@pytest.mark.django_db
def test_chipy_contact_form():  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0

    form_data = {
        "email": "test@test.com",
        "message": "test message",
        "sender": "test",
        "subject": "test subject",
        "captcha_0": "dummy",
        "captcha_1": "PASSED",
    }

    form = ContactForm(form_data)

    assert form.is_valid()
    form.send_email()
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_chipy_contact_view(client):  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0

    response = client.post(
        "/contact/",
        {
            "email": "test@test.com",
            "message": "test message",
            "sender": "test",
            "subject": "test subject",
            "captcha_0": "dummy",
            "captcha_1": "PASSED",
        },
        follow=True,
    )
    assert response.status_code == 200


#    assert b"Your message has been sent to" in response.content
#    assert len(mail.outbox) == 1
