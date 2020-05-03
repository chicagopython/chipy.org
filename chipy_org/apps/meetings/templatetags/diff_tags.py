from django import template
from diff_match_patch import diff_match_patch
from django.utils.safestring import mark_safe

register = template.Library()


def _diff_draft(draft, field):

    topic = draft.topic
    draft_field = getattr(draft, field)
    topic_field = getattr(topic, field)
    if type(draft_field) in [str, int, float]:
        dmp = diff_match_patch()
        diffs = dmp.diff_main(str(topic_field), str(draft_field))
        dmp.diff_cleanupSemantic(diffs)
        return mark_safe(dmp.diff_prettyHtml(diffs))
    else:
        return ""


@register.simple_tag
def diff_draft(**kwargs):
    draft = kwargs['draft']
    field = kwargs['field']
    return _diff_draft(draft, field)
