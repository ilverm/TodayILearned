from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.apps import apps

@receiver(pre_delete, sender='likes.Like')
def decrease_post_likes(sender, instance, **kwargs):
    # Get the Post model
    Post = apps.get_model('posts', 'Post')

    # Decrease the likes field in the related Post
    Post.objects.filter(id=instance.post.id).update(likes=models.F('likes') - 1)