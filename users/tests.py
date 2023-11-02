import re

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(email='temp1@temp.com')
        self.second_user = User.objects.create(email='temp.user@temp.com')

    def test_users_created_correctly(self):
        first_user_pattern = re.match('^([^@]+)', self.first_user.email).group(1)
        second_user_pattern = re.match('^([^@]+)', self.second_user.email).group(1)

        self.assertEqual(first_user_pattern, self.first_user.username)
        self.assertEqual(second_user_pattern, self.second_user.username)