from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from tinymce.widgets import TinyMCE

class PostForm(forms.Form):
    title = forms.CharField(label='Title', required=True)
    slug = forms.CharField(label='Slug', required=True)
    content = forms.CharField(label='Content', required=True, widget=TinyMCE(attrs={'rows': 20}))
    source = forms.URLField(label='Source', required=True)
    tag = forms.CharField(label='Tag', required=True, max_length=25)

    def clean_tag(self):
        if ' ' in super().clean().get('tag'):
            raise ValidationError('Tag field cannot contain spaces.') 
        return self.cleaned_data['tag'].capitalize()
    
    def clean_slug(self):
        self.cleaned_data['slug'] = slugify(self.cleaned_data.get('slug'))
        if len(self.cleaned_data['slug']) > 50:
            raise ValidationError('Slug cannot be longer than 50 characters')
        return self.cleaned_data['slug']
