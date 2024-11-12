# pylint: disable=invalid-name,no-member,unused-variable,duplicate-code,redefined-outer-name
import datetime
import random
import string

import pytest
from django.conf import global_settings
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import override_settings
from django.urls import reverse

from chipy_org.apps.meetings import email
from chipy_org.apps.meetings.models import RSVP, Meeting, Venue
from chipy_org.libs import test_utils

pytestmark = pytest.mark.django_db


@pytest.fixture
def random_meeting_key():
    "returns a alpha numeric string of 40 characterst to comply with the meeting key"
    return "".join(random.choice(string.digits + string.ascii_lowercase) for x in range(40))


@pytest.fixture
def venue():
    v = Venue.objects.create(name="Test")
    return v


@pytest.fixture
def meeting_in_past(random_meeting_key):
    m = Meeting.objects.create(
        when=datetime.date.today() - datetime.timedelta(days=30),
        key=random_meeting_key,
        in_person_capacity=5,
    )
    return m


@pytest.fixture
def meeting_in_future_registration_closed(random_meeting_key):
    m = Meeting.objects.create(
        when=datetime.date.today() + datetime.timedelta(days=30),
        key=random_meeting_key,
        reg_close_date=datetime.date.today() - datetime.timedelta(days=1),
        in_person_capacity=5,
    )
    return m


@pytest.fixture
def meeting_can_register(random_meeting_key):
    m = Meeting.objects.create(
        when=datetime.date.today() + datetime.timedelta(days=30),
        key=random_meeting_key,
        in_person_capacity=2,
        virtual_capacity=2,
    )
    return m


@pytest.fixture
def rsvp(meeting_can_register):
    r = RSVP.objects.create(
        last_name="last name",
        first_name="first_name",
        email="test@test.com",
        meeting=meeting_can_register,
        response=RSVP.Responses.IN_PERSON,
    )
    return r


@pytest.fixture
def rsvp_can_update(meeting_can_register):
    r = RSVP.objects.create(
        last_name="last name",
        first_name="first_name",
        email="test@test.com",
        meeting=meeting_can_register,
        response=RSVP.Responses.IN_PERSON,
    )
    return r


@pytest.fixture
def rsvp_cannot_update(meeting_in_future_registration_closed):
    r = RSVP.objects.create(
        last_name="last name",
        first_name="first_name",
        email="test@test.com",
        meeting=meeting_in_future_registration_closed,
        response=RSVP.Responses.IN_PERSON,
    )
    return r


@pytest.fixture
def rsvp_meeting_in_past(meeting_in_past):
    r = RSVP.objects.create(
        last_name="last name",
        first_name="first_name",
        email="test@test.com",
        meeting=meeting_in_past,
        response=RSVP.Responses.IN_PERSON,
    )
    return r


class MeetingsTest(test_utils.AuthenticatedTest):
    def test_unique_rsvp(self):
        """
        Tests the uniqueness constraints on the rsvp model
        """
        test_venue = Venue.objects.create(name="Test")
        meeting = Meeting.objects.create(
            when=datetime.date.today(), where=test_venue, in_person_capacity=5
        )
        rsvp = RSVP.objects.create(
            user=self.user, meeting=meeting, response=RSVP.Responses.IN_PERSON
        )

        with self.assertRaises(ValidationError):
            # RSVP needs to have a user or name
            rsvp_no_user = RSVP.objects.create(meeting=meeting, response=RSVP.Responses.IN_PERSON)

        with self.assertRaises(ValidationError):
            # This should already exist
            duplicate_rsvp = RSVP.objects.create(
                user=self.user, meeting=meeting, response=RSVP.Responses.IN_PERSON
            )

        with self.assertRaises(ValidationError):
            name_rsvp = RSVP.objects.create(
                name="Test Name",
                meeting=meeting,
                response=RSVP.Responses.IN_PERSON,
                email="dummy@example.com",
            )

            # Can't have two of the same name
            duplicate_name_rsvp = RSVP.objects.create(
                name="Test Name",
                meeting=meeting,
                response=RSVP.Responses.IN_PERSON,
                email="dummy@example.com",
            )


def test_rsvp_works_for_anonymous_user(client, meeting_can_register):
    response = client.post(
        reverse("rsvp"),
        data={
            "meeting": meeting_can_register.id,
            "first_name": "Some",
            "last_name": "Body",
            "email": "somebody@example.com",
        },
    )
    assert response.status_code == 200


def test_rsvp_fails_gracefully_with_missing_data(client, meeting_can_register):
    response = client.post(reverse("rsvp"), data={"meeting": meeting_can_register.id})
    assert response.status_code == 200


def test_can_get_rsvp_update_view_for_meeting_with_open_registration(client, rsvp_can_update):
    response = client.get(reverse("update_rsvp_with_key", args=[rsvp_can_update.key]))
    assert response.status_code == 200


def test_cannot_get_rsvp_update_view_for_past_meeting(client, rsvp_meeting_in_past):
    response = client.get(reverse("update_rsvp_with_key", args=[rsvp_meeting_in_past.key]))
    assert response.status_code == 302


def test_cannot_get_rsvp_update_view_for_closed_meeting(client, rsvp_cannot_update):
    response = client.get(reverse("update_rsvp_with_key", args=[rsvp_cannot_update.key]))
    assert response.status_code == 302


def test_anonymous_rsvp_email(rsvp):
    num_in_outbox = len(mail.outbox)
    email.send_rsvp_email(rsvp)
    assert len(mail.outbox) == num_in_outbox + 1


def test_meeting_rsvp_wait_list_in_person(meeting_can_register):
    assert meeting_can_register.in_person_capacity == 2

    rsvp1 = RSVP.objects.create(
        first_name="one",
        last_name="one",
        email="one@rsvp.com",
        response=RSVP.Responses.IN_PERSON,
        meeting=meeting_can_register,
    )
    rsvp2 = RSVP.objects.create(
        first_name="two",
        last_name="two",
        email="two@rsvp.com",
        response=RSVP.Responses.IN_PERSON,
        meeting=meeting_can_register,
    )
    rsvp3 = RSVP.objects.create(
        first_name="three",
        last_name="three",
        email="three@rsvp.com",
        response=RSVP.Responses.IN_PERSON,
        meeting=meeting_can_register,
    )

    # in person capacity is two confirm 3rd RSVP is wait listed
    assert rsvp1.status == RSVP.Statuses.CONFIRMED
    assert rsvp2.status == RSVP.Statuses.CONFIRMED
    assert rsvp3.status == RSVP.Statuses.WAIT_LISTED

    # rsvp1 declines
    rsvp1.response = RSVP.Responses.DECLILNED
    rsvp1.save()

    rsvp1.refresh_from_db()
    rsvp2.refresh_from_db()
    rsvp3.refresh_from_db()

    assert rsvp1.status == RSVP.Statuses.CONFIRMED and rsvp1.response == RSVP.Responses.DECLILNED
    assert rsvp2.status == RSVP.Statuses.CONFIRMED and rsvp2.response == RSVP.Responses.IN_PERSON
    assert rsvp3.status == RSVP.Statuses.CONFIRMED and rsvp3.response == RSVP.Responses.IN_PERSON

    # rsvp1 changes mind back
    rsvp1.response = RSVP.Responses.IN_PERSON
    rsvp1.save()

    rsvp1.refresh_from_db()
    rsvp2.refresh_from_db()
    rsvp3.refresh_from_db()

    assert rsvp1.status == RSVP.Statuses.WAIT_LISTED and rsvp1.response == RSVP.Responses.IN_PERSON
    assert rsvp2.status == RSVP.Statuses.CONFIRMED and rsvp2.response == RSVP.Responses.IN_PERSON
    assert rsvp3.status == RSVP.Statuses.CONFIRMED and rsvp3.response == RSVP.Responses.IN_PERSON
