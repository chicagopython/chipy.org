import django
from django.test.client import Client
from django.contrib.auth.models import User


class AuthenticatedTest(django.test.TestCase):
    def setUp(self):
        self.client = Client()
        self.users = None

        # create login
        user = User(username='test', first_name='Test',
                    last_name='McTesterson', email='test@example.com')
        user.save()
        user.set_password('test123')
        user.save()

        self.user = user

        # login
        self.client.login(username='test', password='test123')

    def extra_users(self):
        self.users = []
        for i in range(2, 5):
            user = User(username=f'test{i}', first_name=f'Test{i}',
                        last_name='McTesterson',
                        email=f'test{i}@example.com')
            user.save()
            self.users.append(user)
