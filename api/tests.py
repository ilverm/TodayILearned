from users.models import CustomUser
from tags.models import Tag
from posts.models import Post
from api.serializers import PostSerializer, TagSerializer

from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate
from rest_framework.reverse import reverse as rest_reverse

import unittest

class ListCreatePosts(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(
            username='testuser',
            email='temp@temp.com',
            password='test-insecure1',
        )
        self.tag = Tag.objects.create(name='test_tag')
        self.post_data = {
            'id': 'http://testserver/api/posts/1/',
            'title': 'test title',
            'content': 'test content',
            'source': 'http://www.test.com',
            'author': self.user.email,
            'tag': self.tag.name
        }

    def test_get_endpoint(self):
        """
        Test whether the "api_posts" endpoint returns a
        200 OK status code, indicating successful retrieval
        of data  
        """
        url = rest_reverse('api_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('rest_framework.throttling.AnonRateThrottle.get_rate')
    def test_get_anon_throttle_endpoint(self, mock):
        mock.return_value = '1/sec'
        response = self.client.get(rest_reverse('api_posts'))
        # Request should pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(rest_reverse('api_posts'))
        # Request should fail
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    @patch('rest_framework.throttling.UserRateThrottle.get_rate')
    def test_get_logged_in_user_throttle_endpoint(self, mock):
        mock.return_value = '2/sec'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(rest_reverse('api_posts'))
        # Requet should pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(rest_reverse('api_posts'))
        # Requet should pass
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(rest_reverse('api_posts'))
        # Request should fail
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_serializer_post_endpoint(self):
        """
        This test ensures the correct functionality of the
        PostSerializer by assessing its behavior.
        """
        factory = APIRequestFactory()
        request = factory.post(rest_reverse('api_posts'), self.post_data)
        context = {'request': request}
        serializer = PostSerializer(data=self.post_data, context=context)
        if serializer.is_valid(raise_exception=True):
            # is self.post_data['id'][-2] ok to do?
            serializer.save(id=self.post_data['id'][-2], tag=self.tag, author=self.user)
            self.assertEqual(self.post_data, serializer.data)

    def test_serializer_with_missing_argument_post_endpoint(self):
        """
        This test ensures the correct functionality of the
        PostSerializer by assessing its behavior when a
        required argument, specifically "title", is
        missing from the provided data.
        """
        self.client.force_authenticate(user=self.user)
        post_data = {
            'content': 'test content',
            'source': 'http://www.test.com',
            'author': self.user,
            'tag': self.tag.name,
        }
        serializer = PostSerializer(data=post_data)
        self.assertFalse(serializer.is_valid())

    def test_post_endpoint_with_logged_in_user(self):
        """
        This test ensures only logged in users can create
        a post.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(rest_reverse('api_posts'), self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_endpoint_with_logged_out_user(self): 
        """
        The test ensures logged out users can not create
        a post.
        """
        response = self.client.post(rest_reverse('api_posts'), self.post_data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_endpoint(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(rest_reverse('api_posts'), self.post_data)
        response = self.client.delete(path=self.post_data['id'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_serializer_update_endpoint(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(rest_reverse('api_posts'), self.post_data)

        new_data = self.post_data
        new_data['title'] = 'new title'
        new_data_id = new_data['id'][-2]

        response = self.client.put(rest_reverse('api_singlepost', new_data_id), new_data)
        self.assertTrue(response.status_code, status.HTTP_200_OK)

class ListCreateTags(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.tag1 = Tag.objects.create(name='temp')
        self.tag2 = Tag.objects.create(name='temp2')
        self.user = CustomUser.objects.create(
            username='testuser',
            email='temp@temp.com',
            password='test-insecure1'
        )
        self.post_data = {
            'name': 'temp'
        }

    def test_tag_get_endpoint(self):
        """
        Test whether the "api_tags" endpoint returns a
        200 OK status code, indicating successful retrieval
        of data
        """
        url = rest_reverse('api_tags')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_serializer(self):
        """
        This test ensures the correct functionality of the
        TagSerializer by assessing its behavior.
        """
        url = rest_reverse('api_tags')
        response = self.client.get(url)
        expected_data = TagSerializer([self.tag1, self.tag2], many=True).data
        self.assertEqual(response.data, expected_data)
    
    def test_tag_post_endpoint_with_logged_in_user(self):
        """
        Test if the tag is correctly being created with
        logged in user.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/tags/', self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tag_post_endpoint_with_logged_out_user(self):
        """
        Test if the tag is not being created with logged
        out user.
        """
        response = self.client.post('/api/tags/', self.post_data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)