from captcha.fields import ReCaptchaField
from envelope.views import ContactView
from envelope.forms import BaseContactForm


class ChipyContactForm(BaseContactForm):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})


class ChipyContactView(ContactView):
    form_class = ChipyContactForm

