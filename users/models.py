import re

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = models.CharField(max_length=16)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        """
        Save method for the CustomUser model.

        This method is responsible for automatically populating
        the 'username' field based on the 'email' field when
        saving a CustomUser instance.

        The 'username' is derived from the part of the 'email'
        address before the '@' symbol.
        """
        self.username = re.match('^([^@]+)', self.email).group(1)
        super().save(*args, **kwargs)
