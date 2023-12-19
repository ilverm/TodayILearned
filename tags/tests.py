import unittest

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Tag

from posts.models import Post

User = get_user_model()

class TagModelTest(TestCase):

    def setUp(self):
        self.author = User.objects.create(email='test@test.com', username='test')
        self.tag = Tag.objects.create(name='Test')
        self.post = Post.objects.create(
            title='temp post', 
            source='http://www.temp.com', 
            author=self.author,
            tag=self.tag
        )

    def test_tag_str_method(self):
        self.assertEqual(str(self.tag), 'Test')

