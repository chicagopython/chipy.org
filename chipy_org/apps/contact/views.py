from captcha.fields import ReCaptchaField
from envelope.views import ContactView
from envelope.forms import ContactForm


class ChipyContactForm(ContactForm):
    captcha = ReCaptchaField(attrs={'theme': 'clean'})


class ChipyContactView(ContactView):
    form_class = ChipyContactForm

