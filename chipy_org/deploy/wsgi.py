from django.core.wsgi import get_wsgi_application

import pinax.env


# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)


# set application for WSGI processing
from dj_static import Cling

application = Cling(get_wsgi_application())