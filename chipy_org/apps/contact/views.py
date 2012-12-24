from envelope.views import ContactView
from envelope.forms import BaseContactForm

class ChipyContactView(ContactView):
    form_class = BaseContactForm

