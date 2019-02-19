from nocaptcha_recaptcha.fields import NoReCaptchaField
from envelope.views import ContactView
from envelope.forms import ContactForm


class ChipyContactForm(ContactForm):
    captcha = NoReCaptchaField()


class ChipyContactView(ContactView):
    form_class = ChipyContactForm
