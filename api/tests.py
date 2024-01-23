from django.test import TestCase

from users.models import CustomUser

from rest_framework.test import APIClient
from rest_framework import status

import unittest

class PostApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(
            username='testuser',
            email='temp@temp.com',
            password='test-insecure1',
        )
        self.client.force_authenticate(user=self.user)

    def test_post_endpoint(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

