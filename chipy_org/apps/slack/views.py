from django.views.generic.edit import FormView

from .forms import SlackSignupForm


class JoinSlackView(FormView):
    template_name = "slack/join.html"
    form_class = SlackSignupForm
    success_url = "../"

    def form_valid(self, form):
        messages.success(self.request, "Check your email for an invite to Slack")
        return super().form_valid(form)
