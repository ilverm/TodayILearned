from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms

from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')
        
    def validate_username(self):
        if len(self.username) < 8 or ' ' in self.username:
            raise ValidationError("""Username must be at least 8 characters long
                                    and should not contain spaces.""")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username')