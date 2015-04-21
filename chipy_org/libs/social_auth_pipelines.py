from django.utils.translation import ugettext
from social_auth.exceptions import AuthAlreadyAssociated
from social_auth.backends.pipeline.associate import associate_by_email as super_associate_by_email


def associate_by_email(*args, **kwargs):
    """Check if a user with this email already exists. If they do, don't create an account."""
    backend = kwargs['backend']
    if backend.name == 'google-oauth2':
        # We provide and exception here for users upgrading.
        return super_associate_by_email(*args, **kwargs)

    msg = ugettext('This email is already in use. First login with your other account and '
                   'under the top right menu click add account.')
    raise AuthAlreadyAssociated(backend, msg % {
        'provider': backend.name
    })
