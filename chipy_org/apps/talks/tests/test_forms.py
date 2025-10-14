import pytest
from django.contrib.auth.models import User
from django.test import RequestFactory

from chipy_org.apps.meetings.models import Presenter, Topic
from chipy_org.apps.talks.forms import TopicForm

pytestmark = pytest.mark.django_db


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )


@pytest.fixture
def request_with_user(user):
    factory = RequestFactory()
    request = factory.get('/')
    request.user = user
    return request


class TestTopicForm:
    def test_bio_field_required(self, request_with_user):
        """Test that bio field is required"""
        form_data = {
            'title': 'Test Topic',
            'name': 'Test Speaker',
            'email': 'speaker@example.com',
            'phone': '123-456-7890',
            'description': 'Test description',
            'experience_level': 'novice',
            'length': 30,
            # Missing bio field
        }
        form = TopicForm(data=form_data, request=request_with_user)
        assert not form.is_valid()
        assert 'bio' in form.errors

    def test_bio_field_validation_success(self, request_with_user):
        """Test that form is valid when bio field is provided"""
        form_data = {
            'title': 'Test Topic',
            'name': 'Test Speaker',
            'email': 'speaker@example.com',
            'phone': '123-456-7890',
            'description': 'Test description',
            'experience_level': 'novice',
            'length': 30,
            'bio': 'This is a test bio for the speaker.',
            'license': 'CC BY',
        }
        form = TopicForm(data=form_data, request=request_with_user)
        assert form.is_valid(), f"Form errors: {form.errors}"

    def test_bio_saved_to_presenter(self, request_with_user):
        """Test that bio is saved to the presenter when form is saved"""
        form_data = {
            'title': 'Test Topic',
            'name': 'Test Speaker',
            'email': 'speaker@example.com',
            'phone': '123-456-7890',
            'description': 'Test description',
            'experience_level': 'novice',
            'length': 30,
            'bio': 'This is a test bio for the speaker.',
            'license': 'CC BY',
        }
        form = TopicForm(data=form_data, request=request_with_user)
        assert form.is_valid(), f"Form errors: {form.errors}"

        topic = form.save()

        # Check that topic was created
        assert Topic.objects.count() == 1
        assert topic.title == 'Test Topic'

        # Check that presenter was created with bio
        assert Presenter.objects.count() == 1
        presenter = Presenter.objects.first()
        assert presenter.name == 'Test Speaker'
        assert presenter.email == 'speaker@example.com'
        assert presenter.bio == 'This is a test bio for the speaker.'

        # Check that presenter is associated with topic
        assert topic.presenters.count() == 1
        assert topic.presenters.first() == presenter

    def test_bio_field_widget_is_textarea(self, request_with_user):
        """Test that bio field uses Textarea widget"""
        form = TopicForm(request=request_with_user)
        bio_field = form.fields['bio']

        assert bio_field.widget.__class__.__name__ == 'Textarea'
        assert bio_field.widget.attrs['rows'] == 4
        assert bio_field.widget.attrs['cols'] == 50

    def test_bio_field_label(self, request_with_user):
        """Test that bio field has correct label"""
        form = TopicForm(request=request_with_user)
        bio_field = form.fields['bio']

        assert bio_field.label == "Speaker Bio (displayed publicly)"
        assert bio_field.required is True
