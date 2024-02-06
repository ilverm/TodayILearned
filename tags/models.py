from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=80, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name