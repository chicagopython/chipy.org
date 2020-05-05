import datetime
from operator import ne, eq
import pytest
from django.contrib.auth.models import User

from ..models import Topic, TopicDraft, Presentor, Meeting

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "tin,diffs,expected",
    [
        pytest.param({}, {}, eq, id="empty-args"),
        pytest.param({"title": "hi"}, {}, eq, id="min-args-success"),
        pytest.param({"title": "hi"}, {"description": "test"}, ne, id="min-args-fail"),
        pytest.param(
            {
                "title": "hi",
                "description": "test",
                "length_minutes": 5,
                "slides_link": "http://www.chipy.org",
                "experience_level": 0,
            },
            {},
            eq,
            id="max-args-success",
        ),
        pytest.param(
            {
                "title": "hi",
                "description": "test",
                "length_minutes": 5,
                "slides_link": "http://www.chipy.org",
                "experience_level": 0,
            },
            {"description": "test diff"},
            ne,
            id="max-args-fail",
        ),
    ],
)
def test__topic_equals_draft(tin, diffs, expected):
    topic = Topic(**tin)
    topic.save()
    din = {**tin, **diffs}
    draft = TopicDraft(topic=topic, **din)
    draft.save()
    assert expected(topic, draft)


@pytest.mark.freeze_time("2020-04-01")
def test__TopicDraft__publish():
    topic = Topic(title="test")
    topic.notes = "noteA"
    topic.save()
    # create draft
    draft = TopicDraft(topic=topic)
    draft.title = "title"
    draft.experience_level = 1
    draft.slides_link = "http://chipy.org"
    draft.description = "test"
    draft.notes = "noteB"
    draft.save()
    assert topic != draft
    draft.publish()
    assert topic == draft
    assert topic.title == "title"
    assert topic.experience_level == 1
    assert topic.slides_link == "http://chipy.org"
    assert topic.description == "test"
    assert topic.notes == (
        "noteA\n"
        "----------------------------------------------\n"
        "Published Draft 2 on 2020-04-01 00:00:00\n"
        "noteB\n"
        "----------------------------------------------"
    )


def test__TopicQuerySet__get_user_topics():
    user1 = User(username="user1")
    user1.save()
    user2 = User(username="user2")
    user2.save()

    pr1 = Presentor(user=user1, name="u1")
    pr1.save()

    pr2 = Presentor(user=user2, name="u2")
    pr2.save()

    pr3 = Presentor(name="u3")
    pr3.save()

    topic1 = Topic(title="test1")
    topic1.save()
    topic1.presentors.add(pr1)
    topic2 = Topic(title="test2")
    topic2.save()
    topic2.presentors.add(pr2)
    topic3 = Topic(title="test3")
    topic3.save()
    topic3.presentors.add(pr1)
    topic4 = Topic(title="test4")
    topic4.save()
    topic4.presentors.add(pr3)

    assert Topic.objects.get_user_topics(user=user1).count() == 2


@pytest.mark.freeze_time("2020-05-01")
def test__Topic__outstanding():
    meeting1 = Meeting()
    meeting1.when = datetime.datetime(2020, 6, 1)
    meeting1.key = "asdf1"
    meeting1.approved = True
    meeting1.save()

    topic1 = Topic(meeting=meeting1, title="test1")
    topic1.save()
    draft1 = TopicDraft()
    draft1.approved = True
    topic1 >> draft1
    draft2 = TopicDraft()
    draft2.approved = False
    topic1 >> draft2
    draft3 = TopicDraft()
    draft3.approved = False
    topic1 >> draft3

    assert topic1.outstanding().count() == 2
