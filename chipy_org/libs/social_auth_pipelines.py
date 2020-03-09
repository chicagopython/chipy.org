from django.contrib.auth import get_user_model
from django.utils.translation import ugettext
from social_core.exceptions import AuthAlreadyAssociated
from social_core.pipeline.social_auth import associate_by_email as super_associate_by_email


def associate_by_email(*args, **kwargs):
    """Check if a user with this email already exists. If they do, don't create an account."""
    backend = kwargs['backend']
    if backend.name in ['google-oauth2', 'github'] or kwargs.get('user'):
        # We provide and exception here for users upgrading.
        return super_associate_by_email(*args, **kwargs)

    email = kwargs['details'].get('email')

    if email:
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            msg = ugettext('This email is already in use. First login with your other account and '
                           'under the top right menu click add account.')
            raise AuthAlreadyAssociated(backend, msg.format(provider=backend.name))
