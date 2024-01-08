from django.db import models
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.apps import apps

def get_or_none(model, **kwargs):
    """
    Helper function to simplify getting the object
    or to return "None" if it does not exist.
    """
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

@receiver(pre_delete, sender='likes.Like')
def decrease_post_likes(sender, instance, **kwargs):
    # Get the Post model
    Post = apps.get_model('posts', 'Post')

    # Decrease the likes field in the related Post
    obj = get_or_none(Post, id=instance.post.id)
    if obj and obj.likes >= 1:
        obj.likes = F('likes') - 1
        obj.save()
        obj.refresh_from_db()