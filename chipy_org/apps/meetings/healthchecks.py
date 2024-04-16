import datetime
from dataclasses import dataclass

from django.db.models import Sum

_health_checks = []


def perform_health_check(meeting):
    return [result for result in [check(meeting) for check in _health_checks] if result]


@dataclass
class HealthCheckResult:
    level: str
    category: str
    detail: str


def health_check(fn):
    _health_checks.append(fn)


@health_check
def _status(meeting):
    level = None
    if meeting.status == "published":
        level = "success"
        message = "Meeting published"
    else:
        message = "Meeting not published"

    if not level:
        if meeting.when < datetime.datetime.now() + datetime.timedelta(days=60):
            level = "danger"
        elif meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
            level = "warning"
        else:
            level = "secondary"

    return HealthCheckResult(level, "Publish", message)


@health_check
def _location_check(meeting):
    level = "secondary"

    if meeting.where:
        return HealthCheckResult(
            "success", "Location", f"This event has a location: {meeting.where}"
        )

    if meeting.when < datetime.datetime.now() + datetime.timedelta(days=60):
        level = "danger"
    elif meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
        level = "warning"
    else:
        level = "secondary"

    return HealthCheckResult(level, "Location", "No location for meeting")


@health_check
def _meetup_check(meeting):
    if meeting.meetup_id:
        if meeting.__class__.objects.filter(meetup_id=meeting.meetup_id).count() == 1:
            return HealthCheckResult("success", "Meetup", "Unique meetup_id")
        return HealthCheckResult("danger", "Meetup", "Duplicate meetup_id")

    if meeting.when < datetime.datetime.now() + datetime.timedelta(days=60):
        level = "danger"
    elif meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
        level = "warning"
    else:
        level = "secondary"

    return HealthCheckResult(level, "Meetup", "No meetup_id")


@health_check
def _attendance_confirmed(meeting):
    if meeting.capacity_verified:
        return HealthCheckResult("success", "Capacity", "Verified")

    if meeting.when < datetime.datetime.now() + datetime.timedelta(days=60):
        level = "danger"
    elif meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
        level = "warning"
    else:
        level = "secondary"

    return HealthCheckResult(
        level, "Capacity", f"Not verified ({meeting.in_person_capacity} in person)"
    )


@health_check
def _topic_check(meeting):
    from .models import Topic

    count = meeting.topics.filter(status=Topic.StatusChoice.CONFIRMED).count()
    message = f"{count} topics"
    if count >= 2:
        return HealthCheckResult("success", "Topics", message)

    if meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
        level = "danger"
    elif meeting.when < datetime.datetime.now() + datetime.timedelta(days=120):
        level = "warning"
    else:
        level = "secondary"

    unconfirmed_count = meeting.topics.exclude(status=Topic.StatusChoice.CONFIRMED).count()
    if unconfirmed_count:
        message = f"{message} ({unconfirmed_count} unconfirmed)"

    return HealthCheckResult(level, "Topics", message)


@health_check
def _length_check(meeting):
    from .models import Topic

    count = meeting.topics.filter(status=Topic.StatusChoice.CONFIRMED).count()
    total = (
        meeting.topics.filter(status=Topic.StatusChoice.CONFIRMED).aggregate(Sum("length"))[
            "length__sum"
        ]
        or 0
    )
    length = total + (5 * count if count < 4 else 2.5 * count)
    message = f"{length} minutes of programming"
    if length >= 80:
        level = "success"
    elif length <= 30 and meeting.when < datetime.datetime.now() + datetime.timedelta(days=120):
        level = "warning"
    elif length <= 40 and meeting.when < datetime.datetime.now() + datetime.timedelta(days=90):
        level = "danger"
    else:
        level = "secondary"

    return HealthCheckResult(level, "Length", message)
