from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_username(username):
    """
    Username must be at least 8 characters long and cannot
    contain spaces 
    """
    if len(username) < 8 or ' ' in username:
        raise ValidationError(
            _('Username must be at least 8 characters long and must not contain spaces.'))