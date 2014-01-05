from django.conf.urls import url, patterns
from .views import Home

urlpatterns = patterns("main.views",
    url(r'^$', Home.as_view(), name='home'),
)
