from django.db import models

from users.models import CustomUser
from posts.models import Post

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    class Meta:
        # Ensure a user can like/dislike a post only once
        unique_together = ('user', 'post')
