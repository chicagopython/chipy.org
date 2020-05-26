from django.contrib import messages
from django.views.generic.edit import FormView

from chipy_org.apps.contact.forms import ContactForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = "/home/"

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, "Your message has been sent to Chipy's Organizers")
        return super().form_valid(form)
