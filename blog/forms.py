from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser, Comment

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

