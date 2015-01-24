from django.conf.urls import *
from django.views.generic import TemplateView

urlpatterns = patterns("",
    url(r"^$", 'django.contrib.flatpages.views.flatpage', {'url': '/about/'}, name='about'),
    # url(r"^terms/$", TemplateView.as_view(template_name="about/terms.html"), name="terms"),
    # url(r"^privacy/$", TemplateView.as_view(template_name="about/privacy.html"), name="privacy"),
    # url(r"^dmca/$", TemplateView.as_view(template_name="about/dmca.html"), name="dmca"),
)
