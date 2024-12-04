import datetime
import itertools

import pytest
from freezegun import freeze_time

from chipy_org.apps.meetings.models import Meeting, MeetingType

pytestmark = pytest.mark.django_db

@pytest.fixture
def example_published_meeting_set1():

    meet_times = {
        "past_meeting2": datetime.datetime(2023, 11, 1, 0, 0, 0),
        "past_meeting1": datetime.datetime(2023, 12, 1, 0, 0, 0),
        "present_meeting1": datetime.datetime(2024, 1, 1, 0, 0, 0),
        "future_meeting1": datetime.datetime(2024, 2, 1, 0, 0, 0),
        "future_meeting2": datetime.datetime(2024, 3, 1, 0, 0, 0),
        "future_meeting3": datetime.datetime(2024, 4, 1, 0, 0, 0),
    }
    meetings = {}
    for name, time in meet_times.items():
        meetings[name] = Meeting.objects.create(
            status=Meeting.Status.PUBLISHED,
            capacity_verified=True,
            when=time,
            in_person_capacity=100,
            key=f"{name}",
            )
    return meetings


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__future_published__basic(example_published_meeting_set1):
    assert list(
        itertools.chain(*Meeting.objects.future_published().values_list('key'))
        ) == [
            'present_meeting1',
            'future_meeting1',
            'future_meeting2',
            'future_meeting3',
        ]


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__future_published__filter_unpublished(
        example_published_meeting_set1):

    Meeting.objects.update(status=Meeting.Status.DRAFT)
    assert list(
        itertools.chain(*Meeting.objects.future_published().values_list('key'))
        ) == [], "Do not return any values because no meetings published"


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__future_published_main__basic(example_published_meeting_set1):
    assert list(
        itertools.chain(*Meeting.objects.future_published_main().values_list('key'))
        ) == [
            'present_meeting1',
            'future_meeting1',
            'future_meeting2',
            'future_meeting3',
        ]


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__future_published_main__meetings_not_main(
        example_published_meeting_set1):
    sig = MeetingType.objects.create(name="MySIG")
    Meeting.objects.update(meeting_type=sig)
    assert list(
        itertools.chain(*Meeting.objects.future_published_main().values_list('key'))
        ) == [], "No results returned because meeting types are SIG events"


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__past_published__basic(
        example_published_meeting_set1):
    assert list(
        itertools.chain(*Meeting.objects.past_published().values_list('key'))
        ) == [
            'past_meeting1',
            'past_meeting2',
        ], "Return only past published meetings"


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__past_published__filter_unpublished(
        example_published_meeting_set1):
    Meeting.objects.update(status=Meeting.Status.DRAFT)
    assert list(
        itertools.chain(*Meeting.objects.past_published().values_list('key'))
        ) == [], "No meetings are published, so no return."


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__past_year_published(
        ):

    meet_times = {
        "past_meeting3": datetime.datetime(2022, 12, 31, 23, 59, 59),

        "past_meeting2": datetime.datetime(2023, 1, 1, 0, 0, 0),
        "past_meeting1": datetime.datetime(2023, 12, 31, 23, 59, 59),
        "present_meeting1": datetime.datetime(2024, 1, 1, 0, 0, 0),

        "future_meeting1": datetime.datetime(2024, 2, 1, 0, 0, 0),
    }
    meetings = {}
    for name, time in meet_times.items():
        meetings[name] = Meeting.objects.create(
            status=Meeting.Status.PUBLISHED,
            capacity_verified=True,
            when=time,
            in_person_capacity=100,
            key=f"{name}",
            )

    assert list(
        itertools.chain(*Meeting.objects.past_year_published().values_list('key'))
        ) == ["past_meeting2", "past_meeting1", "present_meeting1"], (
            "return meetings within the last 356 days")


@freeze_time("2024-01-1 00:00:00")
def test__Meeting__queryset__next_meeting(
        example_published_meeting_set1):
    assert Meeting.objects.next_meeting().key == 'present_meeting1', (
        "return the next meeting"
    )


@freeze_time("2024-01-1 02:59:00") # 2 hours and 59 minutes after meeting
def test__Meeting__queryset__next_meeting__before_grace_period(
        example_published_meeting_set1,):
    assert Meeting.objects.next_meeting().key == 'present_meeting1', (
        "Meeting should be considered present until 3 hours after meeting start"
    )


@freeze_time("2024-01-1 03:01:00") # 3 hours and 1 minute after meeting
def test__Meeting__queryset__next_meeting__after_grace_period(
        example_published_meeting_set1):
    assert Meeting.objects.next_meeting().key == 'future_meeting1', (
        "3 hours after 'present' meeting has started, we no longer consider it present"
    )
