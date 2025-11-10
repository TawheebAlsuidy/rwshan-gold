from django import forms
from django.utils.translation import gettext_lazy as _
from blog.models.blog_models import Post


class PostSearchForm(forms.Form):
    query = forms.CharField(
        label=_('Search'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Search blog posts...')
        })
    )
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label=_('Category'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from blog.models.blog_models import PostCategory
        self.fields['category'].queryset = PostCategory.objects.all()