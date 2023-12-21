from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget, LazyEncoder
from django import forms
from django.forms.renderers import get_default_renderer
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

JSON_ENCODE = LazyEncoder().encode


class CustomCKEditorWidget(CKEditorWidget):
    def render(self, name, value, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ""
        final_attrs = self.build_attrs(self.attrs, attrs)
        self._set_config()
        external_plugin_resources = [
            [force_str(a), force_str(b), force_str(c)] for a, b, c in self.external_plugin_resources
        ]

        return mark_safe(
            renderer.render(
                "custom_ckeditor/widget.html",
                {
                    "final_attrs": flatatt(final_attrs),
                    "value": conditional_escape(force_str(value)),
                    "id": final_attrs["id"],
                    "config": JSON_ENCODE(self.config),
                    "external_plugin_resources": JSON_ENCODE(external_plugin_resources),
                },
            )
        )


class CustomRichTextField(RichTextField):
    @staticmethod
    def _get_form_class():
        print("in custom text field")
        return CustomRichTextFormField


class CustomRichTextFormField(forms.fields.CharField):
    # pylint: disable=keyword-arg-before-vararg
    def __init__(
        self,
        config_name="default",
        extra_plugins=None,
        external_plugin_resources=None,
        *args,
        **kwargs,
    ):
        kwargs.update(
            {
                "widget": CustomCKEditorWidget(
                    config_name=config_name,
                    extra_plugins=extra_plugins,
                    external_plugin_resources=external_plugin_resources,
                )
            }
        )
        print("in custom form field")
        super().__init__(*args, **kwargs)
