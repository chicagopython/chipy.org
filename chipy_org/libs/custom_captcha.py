from django_recaptcha.widgets import ReCaptchaV2Checkbox


class CrispyReCaptchaV2Checkbox(ReCaptchaV2Checkbox):
    """
    appends CSS class crispy-captcha to this widget
    the crispy-captcha css removes the border and padding
    applied to from the recaptcha widget by crispy-forms
    """

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["class"] = attrs.get("class", "") + " crispy-captcha"
        return attrs
