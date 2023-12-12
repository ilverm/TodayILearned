from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 8 or ' ' in username:
            raise ValidationError("""Username must be at least 8 characters long
                                    and should not contain spaces.""")
        
        return username

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')