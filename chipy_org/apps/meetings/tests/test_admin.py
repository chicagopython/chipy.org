import pytest
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html

from chipy_org.apps.meetings.admin import TopicAdmin
from chipy_org.apps.meetings.models import Presenter, Topic

pytestmark = pytest.mark.django_db


class TestTopicAdmin:
    def test_get_presenter_bios_with_bios(self):
        """Test get_presenter_bios method when presenters have bios"""
        # Create presenters with bios
        presenter1 = Presenter.objects.create(
            name="Speaker One",
            email="speaker1@example.com",
            bio="This is the first speaker's bio."
        )
        presenter2 = Presenter.objects.create(
            name="Speaker Two",
            email="speaker2@example.com",
            bio="This is the second speaker's bio."
        )

        # Create topic and associate presenters
        topic = Topic.objects.create(title="Test Topic")
        topic.presenters.add(presenter1, presenter2)

        # Test the admin method
        admin = TopicAdmin(Topic, AdminSite())
        result = admin.get_presenter_bios(topic)

        expected = format_html("<br>".join([
            "<strong>Speaker One:</strong> This is the first speaker's bio.",
            "<strong>Speaker Two:</strong> This is the second speaker's bio."
        ]))

        assert result == expected

    def test_get_presenter_bios_with_long_bio(self):
        """Test get_presenter_bios method truncates long bios"""
        # Create presenter with long bio
        long_bio = "This is a very long bio that should be truncated. " * 10  # > 100 chars
        presenter = Presenter.objects.create(
            name="Long Bio Speaker",
            email="longbio@example.com",
            bio=long_bio
        )

        topic = Topic.objects.create(title="Test Topic")
        topic.presenters.add(presenter)

        admin = TopicAdmin(Topic, AdminSite())
        result = admin.get_presenter_bios(topic)

        # Should be truncated to 100 chars + "..."
        expected_bio = long_bio[:100] + "..."
        expected = format_html(f"<strong>Long Bio Speaker:</strong> {expected_bio}")

        assert result == expected
        assert len(presenter.bio) > 100  # Verify original bio is long
        assert "..." in result  # Verify truncation occurred

    def test_get_presenter_bios_no_bios(self):
        """Test get_presenter_bios method when no presenters have bios"""
        # Create presenters without bios
        presenter1 = Presenter.objects.create(
            name="Speaker One",
            email="speaker1@example.com"
        )
        presenter2 = Presenter.objects.create(
            name="Speaker Two",
            email="speaker2@example.com"
        )

        topic = Topic.objects.create(title="Test Topic")
        topic.presenters.add(presenter1, presenter2)

        admin = TopicAdmin(Topic, AdminSite())
        result = admin.get_presenter_bios(topic)

        assert result == "No bios available"

    def test_get_presenter_bios_mixed_bios(self):
        """Test get_presenter_bios method when some presenters have bios and others don't"""
        # Create presenters - one with bio, one without
        presenter_with_bio = Presenter.objects.create(
            name="Speaker With Bio",
            email="withbio@example.com",
            bio="This speaker has a bio."
        )
        presenter_without_bio = Presenter.objects.create(
            name="Speaker Without Bio",
            email="withoutbio@example.com"
        )

        topic = Topic.objects.create(title="Test Topic")
        topic.presenters.add(presenter_with_bio, presenter_without_bio)

        admin = TopicAdmin(Topic, AdminSite())
        result = admin.get_presenter_bios(topic)

        # Should only show the presenter with bio
        expected = format_html("<strong>Speaker With Bio:</strong> This speaker has a bio.")
        assert result == expected

    def test_get_presenter_bios_no_presenters(self):
        """Test get_presenter_bios method when topic has no presenters"""
        topic = Topic.objects.create(title="Test Topic")

        admin = TopicAdmin(Topic, AdminSite())
        result = admin.get_presenter_bios(topic)

        assert result == "No bios available"

    def test_get_presenter_bios_short_description(self):
        """Test that get_presenter_bios has correct short_description"""
        admin = TopicAdmin(Topic, AdminSite())
        assert admin.get_presenter_bios.short_description == "Presenter Bios"
