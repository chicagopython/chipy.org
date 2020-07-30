import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def checkbox(checkbox_label):
    # For example, checkbox_label is '<label for="id_is_external_recruiter">Are you an external recruiter?</label>'

    id_regex = re.search('"id_\w+"', checkbox_label)
    checkbox_id = (
        id_regex.group()
    )  # For example, checkbox_id is '"id_is_external_recruiter"', which includes the double quotation marks
    input_name = checkbox_id[4:-1]  # For example, yields the string 'is_external_recruiter'

    label_regex = re.search("^(?P<first>\<.+\>)(?P<second>.+)(?P<third>\<.+\>)$", checkbox_label)
    label_text = label_regex.group("second")

    html = f'<label for={checkbox_id}><input type="checkbox" name="{input_name}" id={checkbox_id} style="vertical-align: top;"> {label_text}</label>'
    return html
