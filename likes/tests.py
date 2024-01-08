import unittest

from django.test import TestCase
from django.db import IntegrityError

from posts.models import Post
from users.models import CustomUser
from tags.models import Tag

from .models import Like
from .signals import get_or_none

class LikeModelTest(TestCase):
    """
    Test cases for the Like model.
    """
    
    def setUp(self):
        self.user = CustomUser.objects.create(username='temp-user', email='temp@temp.com')
        self.tag = Tag.objects.create(name='Temp')
        self.post = Post.objects.create(
            title='temp', 
            source='http://www.temp.com', 
            author=self.user,
            tag=self.tag,
            likes=2
        )

    def test_create_like(self):
        """
        Test creating a Like object with valid data.
        - Creates a Like object and checks if it has the
        correct user, post, and default liked value (False).
        """
        like = Like.objects.create(user=self.user, post=self.post)
        
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.liked, False)
        self.assertEqual(Like.objects.count(), 1)

    def test_create_like_with_liked_true(self):
        """
        Test creating a Like object with the 'liked' field explicitly set to True.
        - Creates a Like object with liked=True and 
        checks if it has the correct values.
        """
        like = Like.objects.create(user=self.user, post=self.post, liked=True)

        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)
        self.assertEqual(like.liked, True)
        self.assertEqual(Like.objects.count(), 1)

    def test_unique_constraint(self):
        """
        Test the unique constraint on the combination of 'user' and 'post'.
        - Creates a Like object.
        - Attempts to create another Like with the same 
        user and post, expecting an IntegrityError.
        """
        Like.objects.create(user=self.user, post=self.post)

        with self.assertRaises(IntegrityError):
            Like.objects.create(user=self.user, post=self.post)

    def test_get_likes_for_user(self):
        """
        Test retrieving likes for a specific user.
        - Creates two Posts and a CustomUser.
        - Creates Like objects for both posts and the user.
        - Retrieves likes for the user and checks if the count
        is correct.
        """
        post1 = Post.objects.create(
            title='temp1',
            source='http://www.temp.com',
            author=self.user,
            tag=self.tag
        )

        post2 = Post.objects.create(
            title='temp2',
            source='http://www.temp.com',
            author=self.user,
            tag=self.tag
        )

        Like.objects.create(user=self.user, post=post1)
        Like.objects.create(user=self.user, post=post2)

        likes_for_user = Like.objects.filter(user=self.user)
        self.assertEqual(likes_for_user.count(), 2)

    def test_get_likes_for_post(self):
        """
        Test retrieving likes for a specific post.
        - Creates two CustomUsers and a Post.
        - Creates Like objects for both users and the post.
        - Retrieves likes for the post and checks if the 
        count is correct.
        """
        user1 = CustomUser.objects.create(username='test1', email='test1@test.com')
        user2 = CustomUser.objects.create(username='test2', email='test2@test.com')
        post = Post.objects.create(
            title='temp',
            source='http://www.temp.com',
            author=user1,
            tag=self.tag
        )

        Like.objects.create(user=user1, post=post, liked=True)
        Like.objects.create(user=user2, post=post, liked=True)

        likes_for_post = Like.objects.filter(post=post)
        self.assertEqual(likes_for_post.count(), 2)

    def test_update_liked_field(self):
        """
        Test updating the 'liked' field of a Like object.
        - Creates a Like object with liked=False.
        - Updates the 'liked' field to True and checks
        if the update is reflected in the database.
        """
        like = Like.objects.create(user=self.user, post=self.post, liked=False)

        like.liked = True
        like.save()

        updated_like = Like.objects.get(user=self.user, post=self.post)
        self.assertTrue(updated_like.liked)

    def test_decrease_post_likes(self):
        like = Like.objects.create(user=self.user, post=self.post, liked=True)
        initial_likes = self.post.likes

        like.delete()

        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.likes, initial_likes - 1)

class LikeSignalTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='temp-user', email='temp@temp.com')
        self.tag = Tag.objects.create(name='Temp')
        self.post = Post.objects.create(
            title='temp', 
            source='http://www.temp.com', 
            author=self.user,
            tag=self.tag,
            likes=2
        )

    def test_get_existing_obj(self):
        """
        Test if the get_or_none function correctly returns
        an existing obj when provided with a valid id.
        """
        obj = get_or_none(Post, id=self.post.id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.id, self.post.id)

    def test_get_nonexistent_obj(self):
        """
        Test if the get_or_none function correctly returns
        None when provided with an id that doesn't exist.
        """
        obj = get_or_none(Post, id=999)
        self.assertIsNone(obj)