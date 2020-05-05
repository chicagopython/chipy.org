from diff_match_patch import diff_match_patch
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _diff_draft(draft, field):

    topic = draft.topic
    draft_field = getattr(draft, field)
    topic_field = getattr(topic, field)
    if isinstance(draft_field, (str, int, float)):
        dmp = diff_match_patch()
        diffs = dmp.diff_main(str(topic_field), str(draft_field))
        dmp.diff_cleanupSemantic(diffs)
        return mark_safe(dmp.diff_prettyHtml(diffs))
    else:
        return (
            mark_safe(
                (
                    "<del style='background:#ffe6e6;'>{}</del>"
                    "<ins style='background:#e6ffe6;'>{}</ins>"
                ).format(str(topic_field), str(draft_field))
            )
            if topic_field != draft_field
            else topic_field
        )


@register.simple_tag
def diff_draft(**kwargs):
    draft = kwargs["draft"]
    field = kwargs["field"]
    return _diff_draft(draft, field)


@register.filter
def draft_equals_published(draft, pub):
    return draft == pub
