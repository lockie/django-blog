from django import forms
from django.contrib.auth.models import User

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'image',
            'tags',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
