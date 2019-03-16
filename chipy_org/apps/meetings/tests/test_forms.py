# pylint: disable=redefined-outer-name,invalid-name
import datetime
import pytest
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from ..forms import TopicForm
from ..models import Topic, Presentor, Meeting


User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_fixture():
    return User.objects.create(username="chipy",)

@pytest.fixture
def meeting_fixture():
    return Meeting.objects.create(
        when=datetime.datetime.now() + datetime.timedelta(days=7))


datas = [
    {
        "title": "test-topic",
        "name": "Test Testerson",
        "email": "email@chipy.org",
        "description": "this is a test",
        "experience_level": "novice",
        "notes": "this is a test",
        "license": "CC BY",
        "length_minutes": '20',
    },
]

@pytest.mark.parametrize("data", datas)
def test__basic_topic_test_form(user_fixture, meeting_fixture, data):
    assert Topic.objects.filter(title="test-topic").count() == 0
    assert Presentor.objects.filter(name="Test Testerson").count() == 0

    factory = RequestFactory()
    request = factory.get('/')
    request.user = user_fixture

    topic_form = TopicForm(request, data=data)

    topic_form.is_valid()
    _ = topic_form.save()

    assert Topic.objects.filter(title="test-topic").count() == 1
    assert Presentor.objects.filter(name="Test Testerson").count() == 1
