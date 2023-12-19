from django.db.models.signals import pre_delete
from django.dispatch import receiver

from tags.models import Tag

@receiver(pre_delete, sender=Tag)
def update_post_on_tag_delete(sender, instance, **kwargs):
    instance.posts_tag.all().update(private=True)