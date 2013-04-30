from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", 'django.contrib.flatpages.views.flatpage', {'url': '/about/'}, name='about'),
    # url(r"^terms/$", direct_to_template, {"template": "about/terms.html"}, name="terms"),
    # url(r"^privacy/$", direct_to_template, {"template": "about/privacy.html"}, name="privacy"),
    # url(r"^dmca/$", direct_to_template, {"template": "about/dmca.html"}, name="dmca"),

)
