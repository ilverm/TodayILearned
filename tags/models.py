from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=80, blank=False)

    def __str__(self):
        return self.name