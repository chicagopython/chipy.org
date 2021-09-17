from django.contrib import messages
from django.views.generic.edit import FormView

from chipy_org.apps.contact.forms import ContactForm


class ContactView(FormView):
    template_name = "contact/contact.html"
    form_class = ContactForm
    success_url = "/contact"
    message_as_modal = True

    def form_valid(self, form):
        try:
            form.send_email()
            messages.success(self.request, "Your message has been sent to Chipy's organizers")
        except Exception:
            messages.error(self.request, "Your message was NOT sent to Chipy's organizers")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """ Used to access message_as_modal in template as context """
        context = super(ContactView, self).get_context_data(**kwargs)
        context.update({'message_as_modal': self.message_as_modal})
        return context
