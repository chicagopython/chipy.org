from django.contrib import messages
from django.views.generic.edit import FormView

from chipy_org.apps.contact.forms import ContactForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            try:
                form.send_email()
                messages.success(self.request, "Your message has been sent to Chipy's organizers")
            except Exception:
                messages.error(self.request, "Your message was NOT sent to Chipy's organizers")
        else:
            messages.error(self.request, "Must authenticate to send emails")
        return super().form_valid(form)
