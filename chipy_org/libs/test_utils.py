from django.utils import unittest
import django
from django.test.client import Client
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

class AuthenticatedTest(django.test.TestCase):
    def setUp(self):
        self.c = Client()
        self.users = None

        # create login
        user = User(username = 'test', first_name = 'Test', last_name = 'McTesterson', email = 'test@example.com')
        user.save()
        user.set_password('test123')
        user.save()

        self.user = user


        # login
        self.c.login(username = 'test', password = 'test123')

    def extra_users(self):
        self.users = []
        for i in range(2,5):
            user = User(username = 'test%s' %(i), first_name = 'Test%s' %(i), last_name = 'McTesterson', email = 'test%s@example.com' %(i))
            user.save()
            self.users.append(user)
