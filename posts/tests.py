import unittest

from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from tags.models import Tag
from likes.models import Like

from .models import Post
from .views import single_post_view, delete_article, update_article, personal_page
from .forms import PostForm, UpdatePostForm

User = get_user_model()

class TestForm(PostForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].max_length = 8

    def clean_slug(self):
        self.cleaned_data['slug'] = slugify(self.cleaned_data.get('slug'))
        if len(self.cleaned_data['slug']) > 8:
            raise ValidationError('Slug cannot be longer than 8 characters.')

class PostViewsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(
            email='temp@temp.com', 
            password='temptemp',
            username='test_username',
        )
        self.client = Client()

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_displays_public_posts(self):
        # Create some test data. If a post's private field
        # is set to False, then it is considered public.
        Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='content', 
            source='http://www.temp.com', 
            author=self.test_user,
            private=False
        )
        Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='content',
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
            slug='test-post-1',
            content='content',
            source='http://www.temp.com',
            author=self.test_user,
            private=True
        )
        Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='content',
            source='http://www.temp.com',
            author=self.test_user,
            private=True
        )

        # Make the request to the home_page view
        response = self.client.get(reverse('home'))

        # Check if the posts are not present in the response context
        self.assertQuerysetEqual(response.context['post_qs'], Post.objects.filter(private=False), ordered=False)

    def test_create_post_view(self):
        response = self.client.post(reverse('create'), {
            'title': 'temp',
            'content': 'content', 
            'source': 'http://www.temp.com', 
            'tag': 'Temp'
            }
        )
        self.assertEqual(response.status_code, 302)
        # add more tests when login functionality is created

    def test_single_post_view_get_method_anonymous_user(self):
        """
        Check if the get method of the single_post_view
        works correctly with anonymous user
        """
        factory = RequestFactory()
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user
        )
        request = factory.get(reverse('single_post', args=(post.created_at.year, post.slug,)))
        request.user = AnonymousUser()
        response = single_post_view(request, post.created_at.year, post.slug)
        self.assertEqual(response.status_code, 200)

    def test_single_post_view_post_method_authenticated_user(self):
        """
        Check if the post method of the single_post_view
        works correctly with authenticated user
        """
        factory = RequestFactory()
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
        )
        like = Like.objects.create(
            user=self.test_user,
            post=post,
            liked=False,
        )
        post_data = {'like': 'Like'}
        self.assertEqual(post.likes, 0)
        request = factory.post(reverse('single_post', args=[post.created_at.year, post.slug]), post_data)
        request.user = self.test_user
        response = single_post_view(request, post.created_at.year, post.slug)
        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.likes, 1)

    def test_single_post_view_does_not_display_private_posts(self):
        tag = Tag.objects.create(name='test')
        post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
            private=True,
            tag=tag
        )
        post2 = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
            private=False,
            tag=tag
        )

        response = self.client.get(reverse(
            'single_post', kwargs={'year': post2.created_at.year, 'slug': post2.slug}
        ))
        self.assertEqual(post2, response.context['single_post'])
        self.assertNotEqual(post1, response.context['single_post'])

    def test_search_view(self):
        first_post = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
        )
        second_post = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
        )
        request = self.client.get(reverse('search'), {'q': '1'})
        self.assertIn(Post.objects.first(), request.context['searched'])
        self.assertNotIn(Post.objects.last(), request.context['searched'])

    def test_post_gets_deleted_correctly(self):
        factory = RequestFactory()
        post = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
        )
        request = factory.get(reverse('delete', kwargs={'slug': post.slug}))
        request.user = self.test_user
        response = delete_article(request, post.slug)
        qs = Post.objects.all()
        self.assertEqual(qs.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_post_gets_updated_correctly(self):
        factory = RequestFactory()
        tag = Tag.objects.create(
            name='temp_tag'
        )
        post = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
            private=True,
            tag=tag
        )
        new_data = {
            'title': 'New title',
            'slug': 'new-slug',
            'content': 'new content',
            'source': post.source,
            'private': False,
            'tag': tag,
        }
        request = factory.post(reverse('update', kwargs={'slug': post.slug}), new_data)
        request.user = self.test_user
        response = update_article(request, post.slug)
        post.refresh_from_db()
        self.assertEqual(post.title, 'New title')
        self.assertEqual(post.slug, 'new-slug')

    def test_personal_page_returns_filtered_articles(self):
        test_user1 = User.objects.create(
            email='temp2@temp2.com', 
            password='temptemp2',
            username='test_username2',
        )
        tag = Tag.objects.create(
            name='temp_tag'
        )
        post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            content='Content',
            source='http://www.temp.com',
            author=self.test_user,
            tag=tag
        )
        post2 = Post.objects.create(
            title='Test Post 2',
            slug='test-post-2',
            content='Content',
            source='http://www.temp.com',
            author=test_user1,
            tag=tag
        )

        response = self.client.get(reverse('personal_page', kwargs={'username': self.test_user.username}))
        self.assertIn(post1, response.context['posts'])

class PostModelTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create(email='temp@temp.com', password='temp')
        self.tag = Tag.objects.create(name='Temp')
        self.post = Post.objects.create(
            title='temp',
            slug='temp',
            content='content',
            source='http://www.temp.com', 
            author=self.test_user,
            tag=self.tag
        )

    def test_post_creation(self):
        # Check if the post was created successfully
        self.assertEqual(self.post.title, 'temp')
        self.assertEqual(self.post.content, 'content')
        self.assertEqual(self.post.source, 'http://www.temp.com')
        self.assertEqual(self.post.author, self.test_user)
        self.assertEqual(self.post.tag.name, 'Temp')
        self.assertEqual(self.post.slug, 'temp')

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
        self.assertIn('slug', form.fields)
        self.assertIn('content', form.fields)
        self.assertIn('source', form.fields)
        self.assertIn('tag', form.fields)

    def test_clean_tag_valid(self):
        # Test the clean tag method with valid data
        form_data = {
            'title': 'temp_title',
            'slug': 'temp-title',
            'content': 'content',
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
            'slug': 'temp-title',
            'content': 'content',
            'source': 'http://www.test.com',
            'tag': 'Test tag'
        }
        form = PostForm(data=form_data)
        # Run the form validation method
        form.is_valid()
        # Check that the clean method raises a ValidationError
        self.assertIn('tag', form.errors)

    def test_clean_valid_slug(self):
        form_data = {
            'title': 'temp title',
            'slug': 'temp-title',
            'content': 'content',
            'source': 'http://www.test.com',
            'tag': 'Test'
        }
        form = PostForm(data=form_data)
        form.is_valid()
        self.assertIsNone(form.errors.get('slug'))

    def test_clean_invalid_slug(self):
        form_data = {
            'title': 'this is a very long title',
            'slug': 'this-is-a-very-long-title',
            'content': 'content',
            'source': 'http://www.test.com',
            'tag': 'test',
        }

        form = TestForm(data=form_data)
        self.assertIsNotNone(form.errors.get('slug'))

    def test_updateform_field_is_not_required(self):
        form_data = {
            'title': 'temp_title',
            'content': 'content',
            'source': 'http://www.test.com',
            'tag': 'Test'
        }
        form = UpdatePostForm(data=form_data)
        self.assertTrue(form.is_valid())