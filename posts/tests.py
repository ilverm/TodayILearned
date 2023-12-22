import unittest

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from tags.models import Tag

from .models import Post
from .forms import PostForm

User = get_user_model()

class PostViewsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(email='temp@temp.com', password='temptemp')
        self.client = Client()
        self.client.force_login(self.test_user)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_displays_public_posts(self):
        # Create some test data. If a post's private field
        # is set to False, then it is considered public.
        Post.objects.create(
            title='Test Post 1', 
            source='http://www.temp.com', 
            author=self.test_user,
            private=False
        )
        Post.objects.create(
            title='Test Post 2', 
            source='http://www.temp.com', 
            author=self.test_user,
            private=False
            )

        # Make the request to the home_page view
        response = self.client.get(reverse('home'))

        # Check if the posts are present in the response context
        self.assertQuerysetEqual(response.context['post_qs'], Post.objects.filter(private=False), ordered=False)

    def test_home_page_does_not_display_private_posts(self):
        # Create some test data
        Post.objects.create(
            title='Test Post 1',
            source='http://www.temp.com',
            author=self.test_user,
            private=True
        )
        Post.objects.create(
            title='Test Post 2',
            source='http://www.temp.com',
            author=self.test_user,
            private=True
        )

        # Make the request to the home_page view
        response = self.client.get(reverse('home'))

        # Check if the posts are not present in the response context
        self.assertQuerysetEqual(response.context['post_qs'], Post.objects.filter(private=False), ordered=False)

    def test_create_post_view(self):
        response = self.client.post(reverse('create'), {'title': 'temp', 'source': 'http://www.temp.com', 'tag': 'Temp'})
        self.assertEqual(response.status_code, 302)
        # add more tests when login functionality is created

    def test_single_post_view(self):
        post = Post.objects.create(
            title='Test Post',
            source='http://www.temp.com',
            author=self.test_user
        )
        response = self.client.get(reverse('single_post', args=(post.pk,)))
        self.assertEqual(response.status_code, 200)

class PostModelTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(email='temp@temp.com', password='temp')
        self.tag = Tag.objects.create(name='Temp')
        self.post = Post.objects.create(
            title='temp', 
            source='http://www.temp.com', 
            author=self.test_user,
            tag=self.tag
        )

    def test_post_creation(self):
        # Check if the post was created successfully
        self.assertEqual(self.post.title, 'temp')
        self.assertEqual(self.post.source, 'http://www.temp.com')
        self.assertEqual(self.post.author, self.test_user)
        self.assertEqual(self.post.tag.name, 'Temp')

    def test_post_str_method(self):
        self.assertEqual(str(self.post), 'temp')

    def test_update_post_on_tag_delete(self):
        self.tag.delete()
        updated_post = Post.objects.get(id=self.post.id)
        self.assertTrue(updated_post.private)

class PostFormTest(TestCase):

    def test_empty_form(self):
        form = PostForm()
        self.assertIn('title', form.fields)
        self.assertIn('source', form.fields)
        self.assertIn('tag', form.fields)

    def test_clean_tag_valid(self):
        # Test the clean tag method with valid data
        form_data = {
            'title': 'temp_title',
            'source': 'http://www.test.com',
            'tag': 'Test'
        }
        form = PostForm(data=form_data)
        # Run the form validation method
        form.is_valid()
        # Check that the clean method does not raise a
        # ValidationError
        self.assertIsNone(form.errors.get('tag'))

    def test_clean_tag_invalid(self):
        # Test the clean tag method with invalid data
        form_data = {
            'title': 'temp_title',
            'source': 'http://www.test.com',
            'tag': 'Test tag'
        }
        form = PostForm(data=form_data)
        # Run the form validation method
        form.is_valid()
        # Check that the clean method raises a ValidationError
        self.assertIn('tag', form.errors)