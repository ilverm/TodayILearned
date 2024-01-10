from django import forms
from django.core.exceptions import ValidationError

from tinymce.widgets import TinyMCE

class PostForm(forms.Form):
    title = forms.CharField(label='Title', required=True)
    content = forms.CharField(label='Content', required=True, widget=TinyMCE)
    source = forms.URLField(label='Source', required=True)
    tag = forms.CharField(label='Tag', required=True, max_length=25)

    def clean_tag(self):
        return self.cleaned_data['tag'].capitalize()

    def clean(self):
        if ' ' in super().clean().get('tag'):
            raise ValidationError({'tag': 'Tag field cannot contain spaces.'})