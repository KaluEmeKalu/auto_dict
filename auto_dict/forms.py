from django.contrib.auth.models import User

from django.forms import TextInput
from django import forms
from .models import Image, Post
# from .models import *

class CreateUserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserLoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']





class UserImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': TextInput(attrs={'placeholder': 'Type Your message', 'id': 'btn-input',
                                       'class': 'form-control input-sm', }),
        }