from django.db import models

from tags.models import Tag

class Post(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.URLField()
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    likes = models.PositiveIntegerField(default=0)
    # If the account gets deleted, the rating given to a post will be set to null --> no rating.
    # rate = models.ForeignKey('rates.Rate', on_delete=models.SET_NULL)
    # If the account gets deleted, the comments will also be deleted
    # comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.title