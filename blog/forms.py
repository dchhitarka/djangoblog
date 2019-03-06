from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        }
        help_texts = {
            'title': 'Title Must be unique.',
        }
        error_messages = {
            'title': {
                'unique': "Title already exist"
            },
        }

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'body': forms.Textarea(attrs={'rows':3, 'cols': 20}),
        }