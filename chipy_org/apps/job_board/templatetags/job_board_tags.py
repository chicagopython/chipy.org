import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()  # pylint: disable=invalid-name


@register.filter(is_safe=True)
@stringfilter
def checkbox(checkbox_label):
    """ This is a template tag for form fields that are boolean, which are checkbox widgets.
     This function will allow the checkbox and text to be inline next to each other in the template.

    For example, checkbox_label
    if '<label for="id_is_external_recruiter">Are you an external recruiter?</label>',
    the checkbox will be shown next to the words 'Are you an external recruiter?' in the template.
    """
    # fmt: off
    id_regex = re.search('"id_\w+"', checkbox_label)  # pylint: disable=anomalous-backslash-in-string
    # fmt: on

    checkbox_id = id_regex.group()
    # For example, checkbox_id is '"id_is_external_recruiter"',
    # which includes the double quotation marks.
    input_name = checkbox_id[4:-1]  # This will yield the string 'is_external_recruiter'

    # fmt: off
    label_regex = re.search("^(?P<first>\<.+\>)(?P<second>.+)(?P<third>\<.+\>)$", checkbox_label)  # pylint: disable=anomalous-backslash-in-string
    # fmt: on
    label_text = label_regex.group("second")

    html = f'<label for={checkbox_id}><input type="checkbox" name="{input_name}" id={checkbox_id} style="vertical-align: top;"> {label_text}</label>'  # pylint: disable=line-too-long
    return html
