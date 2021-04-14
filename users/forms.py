from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
        

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email')


class AuthorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image', 'position', 'about',
            'github', 'facebook', 'instagram', 'twitter')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
