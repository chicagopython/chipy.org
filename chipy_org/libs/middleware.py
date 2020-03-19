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
        backend = getattr(request, 'backend', None)

        if isinstance(exception, SocialAuthBaseException):
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            if backend:
                extra_tags = f"social-auth {getattr(backend, 'name', 'unknown')}"
            else:
                extra_tags = ''
            messages.error(request, message, extra_tags=extra_tags)

            return redirect(url)

        print(traceback.print_exc())
