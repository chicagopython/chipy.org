from django.utils.translation import ugettext
from django.contrib.auth.models import User

from social_auth.backends.pipeline.user import create_user as social_auth_create_user
from social_auth.exceptions import AuthAlreadyAssociated

def create_user(backend, details, response, uid, username, user = None, is_new = False, *args,
                **kwargs):
    '''
    Check if a user with this email already exists. If they do, don't create an account.
    '''

    if not user:
        if User.objects.filter(email = details.get('email')).exists():
            msg = ugettext('This email is already in use. First login with your other account and under the top right menu click add account.')
            raise AuthAlreadyAssociated(backend, msg % {
                'provider': backend.name
            })
        else:
            return social_auth_create_user(backend, details, response, uid, username, user = None, *args, **kwargs)
    else:
        return {}
