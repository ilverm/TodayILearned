from django.db import models

class Post(models.Model):
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.URLField()
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    # If the account gets deleted, the "like" value will be changed back to its default value --> False
    # like = models.ForeignKey('likes.Like', on_delete=models.SET_DEFAULT, default=False)
    # If the account gets deleted, the rating given to a post will be set to null --> no rating.
    # rate = models.ForeignKey('rates.Rate', on_delete=models.SET_NULL)
    # If the account gets deleted, the comments will also be deleted
    # comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.title