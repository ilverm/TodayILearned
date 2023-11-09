import unittest

from django.test import TestCase, Client
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Post
from .forms import PostForm

User = get_user_model()

@unittest.skip(reason='Working')
class PostViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create(email='temp@temp.com', password='temp')

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_displays_posts(self):
        # Create some test data
        Post.objects.create(title='Test Post 1', source='http://www.temp.com', author=self.test_user)
        Post.objects.create(title='Test Post 2', source='http://www.temp.com', author=self.test_user)

        # Make the request to the home_page view
        response = self.client.get(reverse('home'))

        # Check if the posts are present in the response context
        self.assertQuerysetEqual(response.context['post_qs'], Post.objects.all(), ordered=False)

    def test_create_post_view(self):
        response = self.client.post(reverse('create'), {'email': 'temp@temp.com', 'password': 'temp'})
        self.assertEqual(response.status_code, 302)
        # add more tests when login functionality is created

class PostModelTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(email='temp@temp.com', password='temp')
        self.post = Post.objects.create(title='temp', source='http://www.temp.com', author=self.test_user)

    def test_post_creation(self):
        # Check if the post was created successfully
        self.assertEqual(self.post.title, 'temp')
        self.assertEqual(self.post.source, 'http://www.temp.com')
        self.assertEqual(self.post.author, self.test_user)

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'temp')

@unittest.skip(reason='Working')
class PostFormTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(email='temp@temp.com')

    def test_empty_form(self):
        form = PostForm()
        self.assertIn('title', form.fields)
        self.assertIn('source', form.fields)

    def test_form_works_correctly(self):
        form_data = {
            'title': 'temp_title',
            'source': 'http://www.temp.com',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        temp = form.save(commit=False)
        temp.author = self.test_user
        temp.save()
        self.assertEqual(Post.objects.count(), 1)