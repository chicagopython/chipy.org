# -*- coding: utf-8 -*-
import traceback
from django.contrib import messages
from django.shortcuts import redirect

from social_core.exceptions import SocialAuthBaseException
from social_django.middleware import SocialAuthExceptionMiddleware


class ChipySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    '''
    We're overriding this because modern django, when setup
    correctly can handle messages for anonymous users.
    '''
    def process_exception(self, request, exception):
        self.backend = self.get_backend(request, exception)

        if isinstance(exception, SocialAuthBaseException):
            backend_name = str(self.backend)
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            if backend_name:
                extra_tags = u'social-auth %s' % backend_name
            else:
                extra_tags = ''
            messages.error(request, message, extra_tags=extra_tags)

            return redirect(url)

        print(traceback.print_exc())
