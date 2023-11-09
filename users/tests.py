import re

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTestCase(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(email='temp1@temp.com')
        self.second_user = User.objects.create(email='temp.user@temp.com')
        # this should not work because usernames must be unique
        self.third_user = User.objects.create(email='temp1@temp1.com')

    def test_users_created_correctly(self):
        first_user_pattern = re.match('^([^@]+)', self.first_user.email).group(1)
        second_user_pattern = re.match('^([^@]+)', self.second_user.email).group(1)

        self.assertEqual(first_user_pattern, self.first_user.username)
        self.assertEqual(second_user_pattern, self.second_user.username)

        self.assertEqual(User.objects.count(), 3)

    def test_username_must_be_unique(self):
        #third_user_pattern = re.match('^([^@]+)', self.third_user.email).group(1)
        # this should not fail
        self.assertEqual(User.objects.count(), 2)