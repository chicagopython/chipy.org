from django.template import Context, Template
from django.test import TestCase


class TestNH3Templates(TestCase):
    """Test template tags"""

    def test_bleaching(self):
        """Test that unsafe tags are sanitised"""
        context = Context(
            {"some_unsafe_content": '<script>alert("Hello World!")</script>'},
        )
        template_to_render = Template(
            "{% load nh3_tags %}" "{{ some_unsafe_content|nh3 }}"
        )
        rendered_template = template_to_render.render(context)
        self.assertEqual("", rendered_template)

    def test_bleaching_none(self):
        """Test that None is handled properly as an input"""
        context = Context({"none_value": None})
        template_to_render = Template("{% load nh3_tags %}" "{{ none_value|nh3 }}")
        rendered_template = template_to_render.render(context)
        self.assertEqual("None", rendered_template)

    def test_bleaching_tags(self):
        """Test provided tags are kept"""
        context = Context(
            {
                "some_unsafe_content": (
                    "<b><img src='' "
                    "onerror='alert(\\'hax\\')'>"
                    "I'm not trying to XSS you</b>"
                )
            }
        )
        template_to_render = Template(
            "{% load nh3_tags %}" '{{ some_unsafe_content|nh3:"img" }}'
        )
        rendered_template = template_to_render.render(context)
        self.assertInHTML('<img src="">I\'m not trying to XSS you', rendered_template)
