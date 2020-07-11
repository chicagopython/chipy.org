import pytest
from django.conf import global_settings
from django.core import mail
from django.test import override_settings
from nocaptcha_recaptcha.fields import NoReCaptchaField

from .forms import ContactForm


@pytest.fixture
def no_recaptcha(monkeypatch):
    monkeypatch.setenv("NORECAPTCHA_TESTING", "True")
    yield


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_clean_captcha(no_recaptcha):  # pylint: disable=redefined-outer-name
    """
    This example shows how to override the captach for testing purposes used below. The datadict
    passed to the form and subsquently the widget must contatin the g-recaptcha-response with a
    value of passed, and there must ben an environment variable NORECAPTCHA_TESTING set to 'True' to
    by pass the captcha when the form is cleaned.
    """
    field = NoReCaptchaField()
    value = field.widget.value_from_datadict({"g-recaptcha-response": "PASSED",}, {}, {})
    field.clean(value)


@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_chipy_contact_form(no_recaptcha):  # pylint: disable=redefined-outer-name
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
@override_settings(STATICFILES_STORAGE=global_settings.STATICFILES_STORAGE)
def test_chipy_contact_view(client, no_recaptcha):  # pylint: disable=redefined-outer-name
    assert len(mail.outbox) == 0

    response = client.post(
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
