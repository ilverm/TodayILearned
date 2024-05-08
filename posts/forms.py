from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tinymce.widgets import TinyMCE

class PostForm(forms.Form):
    title = forms.CharField(label=_('Title'), required=True)
    slug = forms.CharField(label=_('Slug'), required=True)
    content = forms.CharField(label=_('Content'), required=True, widget=TinyMCE(attrs={'rows': 20}))
    source = forms.URLField(label=_('Source'), required=True)
    tag = forms.CharField(label=_('Tag'), required=True, max_length=25)

    def clean_tag(self):
        if ' ' in super().clean().get('tag'):
            raise ValidationError(_('Tag field cannot contain spaces.')) 
        return self.cleaned_data['tag'].capitalize()
    
    def clean_slug(self):
        self.cleaned_data['slug'] = slugify(self.cleaned_data.get('slug'))
        if len(self.cleaned_data['slug']) > 50:
            raise ValidationError(_('Slug cannot be longer than 50 characters'))
        return self.cleaned_data['slug']
    
class UpdatePostForm(PostForm):
    title = forms.CharField(label=_('Title'), required=False)
    slug = forms.CharField(label=_('Slug'), required=False)
    content = forms.CharField(label=_('Content'), required=False, widget=TinyMCE(attrs={'rows': 20}))
    source = forms.URLField(label=_('Source'), required=False)
    private = forms.BooleanField(label=_('Private'), required=False)
    tag = forms.CharField(label=_('Tag'), required=False, max_length=25)
