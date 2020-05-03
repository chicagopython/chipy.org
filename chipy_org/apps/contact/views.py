from envelope.forms import ContactForm
from envelope.views import ContactView
from nocaptcha_recaptcha.fields import NoReCaptchaField


class ChipyContactForm(ContactForm):
    captcha = NoReCaptchaField()


class ChipyContactView(ContactView):
    form_class = ChipyContactForm
