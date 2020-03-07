import pytest
from django.template import Context, Template
from flatblocks.models import FlatBlock

pytestmark = pytest.mark.django_db


def test_flatblock():
    """
    render a template with a flatblock to ensure the a compatible version of the flatblocks package is 
    installed
    """
    fb = FlatBlock(header="test-header", slug="test-slug", content="test-content",)
    fb.save()

    t = Template(
        """
        {% load flatblocks %}
        {% flatblock "test-slug" %}
        """
    )

    text = t.render(Context())
    assert "test-header" in text
    assert "test-content" in text
